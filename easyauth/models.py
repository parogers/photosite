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

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

APP_TOKEN_LENGTH = 32
USER_CODE_LENGTH = 4

class AppAuthRequest(models.Model):
    """Represents a request from a third-party application to authenticate
    itself with this server, and ultimately obtain an DRF auth token for
    subsequent interactions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_side_token = models.CharField(max_length=APP_TOKEN_LENGTH)
    user_side_token = models.CharField(max_length=APP_TOKEN_LENGTH, default='')
    user_side_code = models.CharField(max_length=USER_CODE_LENGTH)

    expiry_date = models.DateTimeField(default=None)

    @classmethod
    def delete_expired_requests(self):
        expired_req = AppAuthRequest.objects.filter(
            expiry_date__lte=timezone.now())
        for request_obj in list(expired_req):
            request_obj.delete()

