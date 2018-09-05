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
server and obtain a DRF auth token. It also has the side effect of
validating the users email address to the client app.

There are some scenarios to guard against:

   1. User enters the wrong email when registering the app. The user shouldn't
      be able to proceed until they enter an email address they control.
   2. In the case where the user enters the wrong email, the recipient of 
      that email attempts to hijack/steal the original users registration.
   3. A malcious user attempts to register email addresses they don't control.

The registration flow is:

   1. Client app (eg mobile) makes a request to register. It provides only
   an email address.

   2. The server generates a token T, S, and a short numeric code C. It
   returns token T to the client app and emails the provided address with a 
   link containing the token S.

   3. The user clicks on the link in the email to reveal the value of C. The
   server notes that the link was clicked.

   4. The user enters C into the app and clicks okay. The app calls the server, 
   providing the token T and the code C. If everything checks out, (and the 
   server sees that the link was clicked) the server generates a DRF auth 
   token and returns it to the client. The server also marks the email address 
   as being confirmed.

   5. The app can now use the auth token to access the REST api.

This flow requires the end points:

   POST '/begin'
   > { "email" : "the@address.to.use" }
   < { "registration_token" : "..." }

   GET '/obtain-access-code/<S>'
   < { "access_code" : "1234" }

   POST '/complete'
   > { "registration_token" : "...", "access_code" : "..." }
   < { "token" : "..." }
   (token = DRF auth token for future API requests)

"""

import string

from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from django.utils import crypto
from django.urls import reverse
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .models import AppAuthRequest, APP_TOKEN_LENGTH, USER_CODE_LENGTH

# The client app registration end point is split into two API classes,
# so that we can use two different serializers. To begin the registration
# process we only need an email address. To complete the process we need
# an email address, registration token and the short code.
class BeginRegistrationView(APIView):
    class Serializer(serializers.Serializer):
        email = serializers.EmailField()

    serializer_class = Serializer

    def get_view_name(self):
        return 'Begin Registration'

    #def get(self, request):
    #    return Response({'test' : '123'})

    def post(self, request):
        '''Begin the client app registration process. The client supplies an
        email address. (matching a user record) This end point returns a 
        registration token, and emails a short code that can be used to 
        complete the registration.'''

        app_token = crypto.get_random_string(length=APP_TOKEN_LENGTH)
        user_token = crypto.get_random_string(length=APP_TOKEN_LENGTH)
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
            link = request.build_absolute_uri(
                reverse('easyauth:obtain_access_code',
                args=[user_token]))

            print('***')
            print('*** Emailing link: %s' % link)
            print('***')

            request_obj = AppAuthRequest.objects.create(
                user=user,
                app_side_token=app_token,
                user_side_token=user_token,
                user_side_code=user_code)

        return Response({'registration-token' : app_token})

class ObtainAccessCodeView(APIView):
    def get_view_name(self):
        return 'Obtain Access Code'

    #@action(
    #    detail=False,
    #    methods=['get'],
    #    url_path='obtain-access-code/(?P<token>[a-zA-Z0-9]*)')

    def get(self, request, token=None):
        try:
            request_obj = AppAuthRequest.objects.get(user_side_token=token)
        except AppAuthRequest.DoesNotExist:
            return Response({'detail' : 'bad credentials'}, status=400)

        return Response({'access_code' : request_obj.user_side_code})

class CompleteRegistrationView(APIView):
    class Serializer(serializers.Serializer):
        registration_token = serializers.CharField()
        access_code = serializers.CharField()

    serializer_class = Serializer

    def get_view_name(self):
        return 'Complete Registration'

    def post(self, request):
        '''Call to complete the client registration process. The app must
        submit the registration token and short code. On success, this end
        point returns a DRF auth token.'''

        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            request_obj = AppAuthRequest.objects.get(
                app_side_token=serializer.validated_data['registration_token'],
                user_side_code=serializer.validated_data['access_code'])
        except AppAuthRequest.DoesNotExist:
            return Response({'detail' : 'bad credentials'}, status=400)

        request_obj.delete()

        # Generate a DRF auth token the client can use from now and on
        token, created = Token.objects.get_or_create(user=request_obj.user)
        return Response({'token' : token.key})

begin_registration = BeginRegistrationView.as_view()
obtain_access_code = ObtainAccessCodeView.as_view()
complete_registration = CompleteRegistrationView.as_view()
