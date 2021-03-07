from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse


class AdminFilterTests(TestCase):
    fixtures = ['demoproject']

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='sax', email='sax@sax.com', password='top_secret')
        self.user.is_superuser = True
        self.user.save()

    def test_admin_filter_RelatedFieldRadioFilter(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        self.assertTrue(self.client.login(
            username='sax', password='top_secret'))
        response = self.client.get(
            reverse('admin:demoapp_demomodel_relatedfieldradiofilter_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(
            'admin:demoapp_demomodel_relatedfieldradiofilter_changelist') + "?demo_related__id__exact=1")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('admin:demoapp_demomodel_relatedfieldradiofilter_changelist') +
                                   "?demo_related__id__exact=1&demo_related__id__exact=2")
        self.assertEqual(response.status_code, 200)

    def test_admin_RelatedFieldCheckbox(self):
        """
        test if the admin page with RelatedFieldCheckbox filters loads succesfully
        """
        self.assertTrue(self.client.login(
            username='sax', password='top_secret'))
        response = self.client.get(
            reverse('admin:demoapp_demomodel_relatedfieldcheckboxfilter_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(
            'admin:demoapp_demomodel_relatedfieldcheckboxfilter_changelist') + "?demo_related__id__exact=1")
        self.assertEqual(response.status_code, 200)

    def test_admin_UnionFieldListFilter(self):
        """
        test if the admin page with UnionFieldListFilter filters loads succesfully
        """
        self.assertTrue(self.client.login(
            username='sax', password='top_secret'))
        response = self.client.get(
            reverse('admin:demoapp_demomodel_unionfieldlistfilter_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(
            'admin:demoapp_demomodel_unionfieldlistfilter_changelist') + "?demo_related_filter=1%2C2")
        self.assertEqual(response.status_code, 200)

    def test_admin_IntersectionFieldListFilter(self):
        """
        test if the admin page with IntersectionFieldListFilter filter loads succesfully
        """
        self.assertTrue(self.client.login(
            username='sax', password='top_secret'))
        response = self.client.get(
            reverse('admin:demoapp_demomodel_intersectionfieldlistfilter_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(
            'admin:demoapp_demomodel_intersectionfieldlistfilter_changelist') + "?demo_related_filter=1%2C2")
        self.assertEqual(response.status_code, 200)

    def test_admin_TextFieldFilter(self):
        """
        test if the admin page with IntersectionFieldListFilter filter loads succesfully
        """
        self.assertTrue(self.client.login(
            username='sax', password='top_secret'))
        response = self.client.get(
            reverse('admin:demoapp_demomodel_intersectionfieldlistfilter_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(
            'admin:demoapp_demomodel_intersectionfieldlistfilter_changelist') + "?name=ccccc")
        self.assertEqual(response.status_code, 200)
