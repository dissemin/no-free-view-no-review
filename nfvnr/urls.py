"""nfvnr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from signatories import views
from django.views.generic import TemplateView

from django.conf import settings

settings.SETUP_ADMIN_LOGIN()

urlpatterns = [
    path('', views.index, name='index'),
    path('sign', views.SignView.as_view(), name='sign'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('thanks', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    path('confirm', TemplateView.as_view(template_name='confirm.html'), name='confirm'),
    path('faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('confirm/<str:token>', views.confirm_email, name='confirm_email'),
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
