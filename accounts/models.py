from django.db import models
from django.contrib.auth.models import User

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField(null=True, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    email_method = models.CharField(
        max_length=20,
        choices=[('gmail', 'Gmail'), ('outlook', 'Outlook')],
        blank=True
    )

    def __str__(self):
        return self.user.username
