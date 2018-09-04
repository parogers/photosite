# photosite - A minimalist django site for posting photos
# Copyright (C) 2018  Peter Rogers (peter.rogers@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This end point allows third-party client apps to register with this
server and obtain a DRF auth token. The registration flow is:

1. Client app (eg mobile) makes a request to register. It provides only
an email address. (this assumes the user has already been registered

2. The server generates a long token T, and a short numeric code C. It
returns the token to the client app, and emails the code to the provided
email address.

3. The user obtains the code from their email and types it into the app.

4. The app calls the server, providing the token T and the code C. If
everything checks out, the server generates a DRF auth token and returns
it to the client. The server also marks the email address as being 
confirmed.

5. The app can now use the auth token to access the REST api."""

import string

from django.contrib.auth.models import User
from django.utils import crypto
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import AppAuthRequest, APP_TOKEN_LENGTH, USER_CODE_LENGTH

# The client app registration end point is split into two viewset classes,
# so that we can use two different serializers. To begin the registration
# process we only need an email address. To complete the process we need
# an email address, registration token and the short code.
class BeginRegistrationViewSet(viewsets.ViewSet):
    class Serializer(serializers.Serializer):
        email = serializers.EmailField()

    serializer_class = Serializer

    def get_view_name(self):
        return 'Begin Registration'

    def create(self, request):
        '''Begin the client app registration process. The client supplies an
        email address. (matching a user record) This end point returns a 
        registration token, and emails a short code that can be used to 
        complete the registration.'''

        app_token = crypto.get_random_string(length=APP_TOKEN_LENGTH)
        user_code = crypto.get_random_string(
            length=USER_CODE_LENGTH,
            allowed_chars=string.digits)

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            # We don't want to raise an error here. That would give a malicious
            # client an easy way to check if an email account is registered
            # with our server.
            pass
        else:
            # The user checks out. Email the confirmation code and make
            # note of this pending registration request.

            # TODO - emailing should be handled as a background task (eg celery)
            print('''*** Emailing short code: %s''' % user_code)

            request_obj = AppAuthRequest.objects.create(
                user=user,
                app_side_token=app_token,
                user_side_code=user_code)

        return Response({'registration-token' : app_token})

class CompleteRegistrationViewSet(viewsets.ViewSet):
    class Serializer(serializers.Serializer):
        email = serializers.EmailField()
        registration_token = serializers.CharField(source='registration-token')
        access_code = serializers.CharField(source='access-code')

    serializer_class = Serializer

    def get_view_name(self):
        return 'Complete Registration'

    @action(detail=False, methods=['put'])
    def complete(self, request):
        '''Call to complete the client registration process. The app must
        submit the registration token and short code. On success, this end
        point returns a DRF auth token.'''
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            request_obj = AppAuthRequest.objects.get(
                app_side_token=serializer.validated_data['registration-token'],
                user_side_code=serializer.validated_data['access-code'],
                user__email=serializer.validated_data['email'])
        except AppAuthRequest.DoesNotExist:
            return Response({'detail' : 'bad credentials'})

        print(request_obj)
        return Response({'token' : '123'})
