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

