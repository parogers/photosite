from django.contrib.auth.models import User
from django.db import models

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

    # TODO - add expiry time
