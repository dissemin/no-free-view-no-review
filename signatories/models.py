from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
    email = models.CharField(max_length=256, null=True, blank=True, db_index=True)
    send_updates = models.BooleanField(default=True)
    verified = models.BooleanField(default=True)
    verification_hash = models.CharField(max_length=64, null=True, blank=True)

    def orcid_url(self):
        return 'https://' + settings.ORCID_BASE_DOMAIN + '/' + self.orcid

    def send_confirmation_email(self, request):
        context = {
            'name': self.name,
            'pledge_title': settings.PLEDGE_TITLE,
            'email': self.email,
            'affiliation': self.affiliation,
            'homepage': self.homepage,
            'organizers_email': settings.ORGANIZERS_EMAIL,
            'request': request,
            'confirmation_link': reverse('confirm_email', args=[self.verification_hash])
        }
        message = render_to_string('confirmation_email.txt', context)
        send_mail(
            'Email confirmation for "{}"'.format(settings.PLEDGE_TITLE),
            message,
            settings.CONFIRMATION_SENDING_EMAIL,
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Signatories"
