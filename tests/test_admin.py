from demo.models import DemoModel, DemoModelField, DemoRelated
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse


class AdminFilterTests(TestCase):
    def setUp(self):
        from demo.utils import DATA
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='sax', email='sax@sax.com', password='top_secret')
        self.user.is_superuser = True
        self.user.save()
        for i in range(3):
            values = DATA.copy()
            values['unique'] = i
            # values['flags'] = {"int": i}
            DemoModelField.objects.create(**values)
        # DemoModelField.objects.create(char="a1", unique=1, **DATA)
        related1 = DemoRelated.objects.create(name='related1')
        related2 = DemoRelated.objects.create(name='related2')
        related3 = DemoRelated.objects.create(name='related3')
        DemoModel.objects.create(name="name1", demo_related=related1, flags={"v": 1})
        DemoModel.objects.create(name="name1.1", demo_related=related1, flags={"v": 1})
        DemoModel.objects.create(name="name2", demo_related=related2, flags={"v": 2})
        DemoModel.objects.create(name="name2.2", demo_related=related2, flags={"v": '2'})
        DemoModel.objects.create(name="nameNone", demo_related=related3, flags={})

    def test_admin_filter_RelatedFieldRadioFilter(self):
        """
        test if the admin page with RelatedFieldRadioFilter filters loads succesfully
        """
        self.assertTrue(self.client.login(
            username='sax', password='top_secret'))
        response = self.client.get(
            reverse('admin:demo_demomodel_relatedfieldradiofilter_changelist'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(
            'admin:demo_demomodel_relatedfieldradiofilter_changelist') + "?demo_related__id__exact=1")
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('admin:demo_demomodel_relatedfieldradiofilter_changelist') +
                                   "?demo_related__id__exact=1&demo_related__id__exact=2")
        self.assertEqual(response.status_code, 200)

    def test_admin_filter_RelatedFieldCheckBoxFilter(self):
        """
        test if the admin page with RelatedFieldCheckBoxFilter filters loads succesfully
        """
        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        base_url = reverse('admin:demo_demomodel_relatedfieldcheckboxfilter_changelist')
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(base_url + "?demo_related__id__exact=1")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(base_url + "?demo_related__id__exact=1&demo_related__id__exact=2")
        self.assertEqual(response.status_code, 200)

    def test_admin_RelatedFieldCheckbox(self):
        """
        test if the admin page with RelatedFieldCheckbox filters loads succesfully
        """
        base_url = reverse('admin:demo_demomodel_relatedfieldcheckboxfilter_changelist')

        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(base_url + "?demo_related__id__exact=1")
        self.assertEqual(response.status_code, 200)

    def test_admin_UnionFieldListFilter(self):
        """
        test if the admin page with UnionFieldListFilter filters loads succesfully
        """
        base_url = reverse('admin:demo_demomodel_unionfieldlistfilter_changelist')

        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(base_url + "?demo_related_filter=1%2C2")
        self.assertEqual(response.status_code, 200)

    def test_admin_IntersectionFieldListFilter(self):
        """
        test if the admin page with IntersectionFieldListFilter filter loads succesfully
        """
        base_url = reverse('admin:demo_demomodel_unionfieldlistfilter_changelist')
        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(base_url + "?demo_related_filter=1%2C2")
        self.assertEqual(response.status_code, 200)

    def test_admin_TextFieldFilter(self):
        """
        test if the admin page with IntersectionFieldListFilter filter loads succesfully
        """
        base_url = reverse('admin:demo_demomodel_intersectionfieldlistfilter_changelist')
        self.assertTrue(self.client.login(username='sax', password='top_secret'))

        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(base_url + "?name=ccccc")
        self.assertEqual(response.status_code, 200)

    def test_admin_JsonFieldFilter(self):
        """
        test if the admin page with IntersectionFieldListFilter filter loads succesfully
        """
        base_url = reverse('admin:demo_demomodel_changelist')
        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(base_url + "?flags__key=v&flags__value=1")
        self.assertEqual(response.status_code, 200)

    def test_admin_NumberFilter(self):
        """
        test if the admin page with IntersectionFieldListFilter filter loads succesfully
        """
        base_url = reverse('admin:demo_demomodelfield_changelist')
        self.assertTrue(self.client.login(username='sax', password='top_secret'))
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(base_url + "?integer=1")
        self.assertEqual(response.status_code, 200)
