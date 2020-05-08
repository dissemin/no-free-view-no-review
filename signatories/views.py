from django.shortcuts import render
from django import forms
from django.conf import settings
from django.db import IntegrityError
from .models import Signatory
from .orcid import form_data_from_orcid_json
from allauth.socialaccount.models import SocialAccount
from captcha.fields import CaptchaField
from django.utils.http import urlencode
from django.views.generic.edit import FormView

def get_user_orcid(user):
    if not user.is_authenticated:
        return None
    try:
        return user.socialaccount_set.get().uid
    except SocialAccount.DoesNotExist:
        return None

def index(request):
    user_orcid = get_user_orcid(request.user)

    this_uri = request.build_absolute_uri()
    signatory_saved = request.META.get('HTTP_REFERER') == this_uri + 'sign'
    social_links = {
        'twitter': 'https://twitter.com/share?' + urlencode({
            'url': this_uri,
            'text': settings.PLEDGE_TITLE,
            'hashtag': settings.PLEDGE_HASHTAG}),
        'facebook': 'http://www.facebook.com/sharer/sharer.php?' + urlencode({
            'u': this_uri,
        }),
        'reddit': 'https://reddit.com/submit?' + urlencode({
            'url': this_uri,
            'title': settings.PLEDGE_TITLE,
        }),
        'email': 'mailto:?' + urlencode({
            'subject': settings.PLEDGE_TITLE,
            'body': this_uri,
        }).replace('+', '%20'),
    }

    context = {
        'pledge_title': settings.PLEDGE_TITLE,
        'social_links': social_links,
        'signatories': Signatory.objects.all().order_by('timestamp'),
        'pledge_signed': signatory_saved or (user_orcid and Signatory.objects.filter(orcid=user_orcid).exists())
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'pledge_title': settings.PLEDGE_TITLE
    }
    return render(request, 'about.html', context)

def faq(request):
    context = {
        'pledge_title': settings.PLEDGE_TITLE
    }
    return render(request, 'faq.html', context)

class SignatoryBaseForm(forms.Form):
    name = forms.CharField(required=True, label='Name', max_length=256)
    affiliation = forms.CharField(required=False, label='Affiliation (optional)', max_length=256)
    homepage = forms.URLField(required=False, label='Homepage (optional)', max_length=512)

class SignatoryManualForm(SignatoryBaseForm):
    email = forms.EmailField(required=True, label='Email')
    send_updates = forms.BooleanField(label='Send me occasional updates about this initiative', required=False)
    captcha = CaptchaField()

class SignatoryOrcidForm(SignatoryBaseForm):
    email = forms.EmailField(required=False, label='Email (optional)')
    send_updates = forms.BooleanField(label='Send me occasional updates about this initiative', required=False)

class SignView(FormView):
    template_name = 'sign.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pledge_title'] = settings.PLEDGE_TITLE
        return context

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return SignatoryOrcidForm
        else:
            return SignatoryManualForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            orcid_profile = self.request.user.socialaccount_set.get().extra_data
            initial.update(form_data_from_orcid_json(orcid_profile, self.request.user.email))
        return initial

    def form_valid(self, form):
        user = self.request.user if self.request.user.is_authenticated else None
        user_orcid = get_user_orcid(self.request.user)
        signatory = Signatory(
            name=form.cleaned_data['name'],
            affiliation=form.cleaned_data['affiliation'],
            homepage=form.cleaned_data['homepage'],
            user=user,
            orcid=user_orcid,
            email=form.cleaned_data['email'],
            send_updates=form.cleaned_data['send_updates'])
        try:
            signatory.save()
        except IntegrityError:
            # Already signed
            pass
        return super().form_valid(form)


