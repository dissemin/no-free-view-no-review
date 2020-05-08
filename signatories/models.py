from django.db import models
from django.conf import settings

class Signatory(models.Model):
    """
    Represents the signature of the pledge by a user
    """
    name = models.CharField(max_length=256)
    affiliation = models.CharField(max_length=256, null=True, blank=True)
    homepage = models.URLField(max_length=512, null=True, blank=True)
    timestamp = models.DateField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    orcid = models.CharField(max_length=20, null=True, blank=True, unique=True)
    email = models.CharField(max_length=256, null=True, blank=True, unique=True)
    send_updates = models.BooleanField(default=True)

    def orcid_url(self):
        return 'https://' + settings.ORCID_BASE_DOMAIN + '/' + self.orcid
