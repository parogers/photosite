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

from django.dispatch import receiver
from django.urls import reverse
from corsheaders.signals import check_request_enabled

@receiver(check_request_enabled)
def allow_api_requests(sender, request, **kwargs):
    # Make sure everything under the API root is accessible from every
    # origin. In the corsheader middleware this actually adds the HTTP client
    # "Origin" value into the "Access-Control-Allow-Origin" response header.
    return request.path.startswith(reverse('api-root'))
