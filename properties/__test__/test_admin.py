from django.contrib.admin.sites import site
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from properties.models import Location, Accommodation, LocalizeAccommodation


class AdminSiteTests(TestCase):
    def setUp(self):
        # Create a superuser
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpassword'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpassword')

        # Create a test user and objects
        self.user = User.objects.create_user(username='testuser', password='password')
        self.location = Location.objects.create(
            id="US",
            title="United States",
            center="POINT(-98.35 39.50)",
            location_type="country",
            country_code="US",
            state_abbr=None,
            city=None
        )
        self.accommodation = Accommodation.objects.create(
            id="accommodation1",
            title="Beautiful House",
            country_code="US",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=150.00,
            center="POINT(-118.245 34.0522)",
            location=self.location,
            user=self.user,
            published=True
        )
        self.localize_accommodation = LocalizeAccommodation.objects.create(
            accommodation=self.accommodation,
            language="en",
            description="A beautiful house in California",
            policy={"pet_policy": "No pets allowed"}
        )

    def test_admin_login(self):
        """
        Test that an admin user can log in and access the admin site.
        """
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)

    def test_location_admin_list_view(self):
        """
        Test that the Location list view works in the admin.
        """
        url = reverse('admin:properties_location_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.location.title)

    def test_location_admin_change_view(self):
        """
        Test that the Location change view works in the admin.
        """
        url = reverse('admin:properties_location_change', args=[self.location.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.location.title)

    def test_accommodation_admin_list_view(self):
        """
        Test that the Accommodation list view works in the admin.
        """
        url = reverse('admin:properties_accommodation_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.accommodation.title)

    def test_accommodation_admin_change_view(self):
        """
        Test that the Accommodation change view works in the admin.
        """
        url = reverse('admin:properties_accommodation_change', args=[self.accommodation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.accommodation.title)

    def test_localize_accommodation_admin_list_view(self):
        """
        Test that the LocalizeAccommodation list view works in the admin.
        """
        url = reverse('admin:properties_localizeaccommodation_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.localize_accommodation.language)

    def test_localize_accommodation_admin_change_view(self):
        """
        Test that the LocalizeAccommodation change view works in the admin.
        """
        url = reverse('admin:properties_localizeaccommodation_change', args=[self.localize_accommodation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.localize_accommodation.description)
