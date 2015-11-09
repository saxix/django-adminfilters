from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class AdminFilterTests(TestCase):
    fixtures = ['demoproject']
    def setUp(self):
                # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='sax', email='sax@sax.com', password='top_secret')
        self.user.is_superuser = True
        self.user.save()


    def test_admin_filter_relatedfieldradiofilter(self):
        """
        test if the admin page with filters loads succesfully
        """
        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(reverse('admin:demoapp_demomodel_relatedfieldradiofilter_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_admin_relatedfieldcheckboxfilter(self):
        """
        test if the admin page with filters loads succesfully
        """
        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(reverse('admin:demoapp_demomodel_relatedfieldcheckboxfilter_changelist'))
        self.assertEqual(response.status_code, 200)
