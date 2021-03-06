
import json
import html5validate
import unittest

from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

from signatories.orcid import name, institution, jpath, urlize, homepage, form_data_from_orcid_json
from signatories.views import get_user_orcid, SignatoryOrcidForm
from signatories.models import Signatory

def loadProfile(id):
    path = 'signatories/fixtures/orcid/{}.json'.format(id)
    with open(path, 'r') as f:
        return json.loads(f.read())


class OrcidTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.antonin = loadProfile(id='0000-0002-8612-8827')
        cls.thomas = loadProfile(id='0000-0003-0524-631X')
        cls.sergey = loadProfile(id='0000-0003-3397-9895')
        cls.marco = loadProfile(id='0000-0002-6561-5642')
        cls.dario = loadProfile(id='0000-0001-9547-293X')
        cls.qiang = loadProfile(id='0000-0001-5006-3868')

    def test_simple_name(self):
        self.assertEqual(name(self.antonin), 'Antonin Delpeuch')
        self.assertEqual(name(self.thomas), 'Thomas Bourgeat')
        self.assertEqual(name(self.marco), 'Marco Diana')

    def test_credit_name(self):
        self.assertEqual(name(self.sergey), 'Sergey M. Natanzon')
        self.assertEqual(name(self.dario), 'Darío Álvarez')

    def test_empty_lastname(self):
        self.assertEqual(name(self.qiang), 'qiang')

    def test_institution(self):
        self.assertEqual(institution(loadProfile(
            id='0000-0002-0022-2290')),
            'Ecole Normale Superieure')
        self.assertEqual(institution(loadProfile(
            id='0000-0002-5654-4053')),
             "École nationale supérieure de céramique industrielle")

    def test_jpath(self):
        self.assertEqual(jpath('awesome', {}), None)
        self.assertEqual(jpath('awesome', {}, 41), 41)
        self.assertEqual(jpath('a', {'a': 'b'}, 41), 'b')
        self.assertEqual(jpath('a/b', {'a': {'b': 7}, 'c': None}, 41), 7)
        self.assertEqual(jpath('a', {'a': {'b': 7}, 'c': None}, 41), {'b': 7})

    def test_urlize(self):
        self.assertEqual(urlize('gnu.org'), 'http://gnu.org')
        self.assertTrue(urlize(None) is None)
        self.assertEqual(urlize(u'https://gnu.org'), 'https://gnu.org')

    def test_homepage(self):
        self.assertEqual(homepage(self.antonin), 'http://antonin.delpeuch.eu/')
        self.assertEqual(homepage(loadProfile(id='0000-0002-5710-3989')), 'http://evrard.perso.enseeiht.fr')

    def test_form_data_from_orcid_json(self):
        self.assertEqual(form_data_from_orcid_json(self.antonin, 'my@email.com'),
            {'name':'Antonin Delpeuch',
             'affiliation': 'University of Oxford',
             'homepage': 'http://antonin.delpeuch.eu/',
             'email': 'my@email.com',
             'send_updates': False})


class ViewsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(ViewsTest, cls).setUpClass()
        cls.orcid_user = User.objects.create_user('dario')
        cls.orcid_id = '0000-0001-9547-293X'
        SocialAccount(
            user=cls.orcid_user,
            provider='orcid',
            uid=cls.orcid_id,
            extra_data=loadProfile(cls.orcid_id)).save()
        cls.other_user = User.objects.create_user('super')

        Signatory(name='John Doe',
            affiliation='NSU',
            homepage='https://gnu.org',
            orcid='0000-0001-2345-6789'
        ).save()
        Signatory(name='Jane Darnell',
        ).save()


    def test_get_user_orcid(self):
        self.assertTrue(get_user_orcid(self.other_user) is None)
        self.assertEqual(get_user_orcid(self.orcid_user), self.orcid_id)

        class DummyUser(object):
            is_authenticated = False
        self.assertTrue(get_user_orcid(DummyUser()) is None)

    def test_index(self):
        resp = self.client.get(reverse('index'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)

    def test_about(self):
        resp = self.client.get(reverse('about'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)

    def test_faq(self):
        resp = self.client.get(reverse('faq'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)

    def test_thanks(self):
        resp = self.client.get(reverse('thanks'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)

    def test_confirm(self):
        resp = self.client.get(reverse('confirm'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)

    def test_visuals(self):
        resp = self.client.get(reverse('visuals'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)

    def test_sign_logged_out(self):
        self.client.logout()
        resp = self.client.get(reverse('sign'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)
        # Without login, we require a captcha
        self.assertTrue('captcha' in resp.content.decode('utf-8'))

    def test_sign_logged_in(self):
        self.client.force_login(self.orcid_user)
        resp = self.client.get(reverse('sign'), follow=True)
        self.assertEqual(resp.status_code, 200)
        html5validate.validate(resp.content)
        # Users who log in via ORCID don't get a captcha
        self.assertFalse('captcha' in resp.content.decode('utf-8'))
        # And the form is prefilled with info obtained from ORCID
        self.assertTrue('Darío' in resp.content.decode('utf-8'))

    def test_submit_logged_in(self):
        # Add a signature while logged in via ORCID
        self.client.force_login(self.orcid_user)
        self.client.post(reverse('sign'),
            {'name':'Dario The King',
             'affiliation':'JHU'})
        # Check that the supplied name and ORCID appear in the list
        resp = self.client.get(reverse('index'), follow=True)
        text = resp.content.decode('utf-8')
        self.assertTrue('Dario The King' in text)
        self.assertTrue(self.orcid_id in text)

    def test_submit_logged_in_after_manually_signed(self):
        # Assume we already have a verified manual signature from Dario
        Signatory(name='Dario Manfred',
            affiliation='NSU',
            homepage='https://gnu.org',
            email='dario@king.com',
            verified=True
        ).save()

        # It appears in the list
        resp = self.client.get(reverse('index'), follow=True)
        text = resp.content.decode('utf-8')
        self.assertTrue('Dario Manfred' in text)
        self.assertTrue('NSU' in text)

        # Add a signature while logged in via ORCID
        self.client.force_login(self.orcid_user)
        self.client.post(reverse('sign'),
            {'name':'Dario The King',
             'affiliation':'JHU',
             'email':'dario@king.com'})
        # Check that the supplied name and ORCID appear in the list
        resp = self.client.get(reverse('index'), follow=True)
        text = resp.content.decode('utf-8')
        self.assertTrue('Dario The King' in text)
        self.assertTrue('Dario Manfred' not in text)
        self.assertTrue(self.orcid_id in text)


    def test_submit_not_logged_in(self):
        self.client.logout()
        self.client.post(reverse('sign'),
            {'name':'Dario The King',
             'affiliation': 'ENS',
             'email': 'dario@foo.com',
             'captcha_0': 'PASSED',
             'captcha_1': 'PASSED'
             })

        # Initially the signature is not verified
        self.assertFalse(Signatory.objects.get(email='dario@foo.com').verified)

        # Check that a verification email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue('Email confirmation' in mail.outbox[0].subject)
        self.assertTrue('The King' in mail.outbox[0].body)

        # Visit the verification link
        s = Signatory.objects.get(email='dario@foo.com')
        self.client.get(reverse('confirm_email', args=[s.verification_hash]))

        # Now the signature should be verified
        self.assertTrue(Signatory.objects.get(email='dario@foo.com').verified)


    def test_orcid_update_without_email(self):
        form = SignatoryOrcidForm(data={'name':'John Doe', 'affiliation':'ENS', 'homepage':'https://gnu.org/', 'send_updates':'checked'})
        self.assertFalse(form.is_valid())
        form = SignatoryOrcidForm(data={'name':'John Doe', 'affiliation':'ENS', 'homepage':'https://gnu.org/', 'send_updates':False})
        self.assertTrue(form.is_valid())
        form = SignatoryOrcidForm(data={'name':'John Doe', 'affiliation':'ENS', 'homepage':'https://gnu.org/', 'send_updates':True, 'email':'john@doe.com'})
        self.assertTrue(form.is_valid())
