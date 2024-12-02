from django.test import TestCase
from django.contrib.auth.models import User
from properties.models import Location, Accommodation, LocalizeAccommodation
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            id="US",
            title="United States",
            center="POINT(-98.35 39.50)",  # Longitude and Latitude for the center of the country
            location_type="country",
            country_code="US",
            state_abbr=None,
            city=None
        )

    def test_location_creation(self):
        """
        Test the creation of the Location model.
        """
        self.assertEqual(Location.objects.count(), 1)
        location = Location.objects.get(id="US")
        self.assertEqual(location.title, "United States")
        self.assertEqual(location.location_type, "country")

    def test_location_str(self):
        """
        Test the string representation of the Location model.
        """
        self.assertEqual(str(self.location), "United States (country)")

    def test_location_invalid(self):
        """
        Test that creating a Location without required fields raises a validation error.
        """
        location = Location(
            id="CA",
            title="California",
            center="POINT(-119.4179 36.7783)",  # Longitude and Latitude for California
            location_type="state",
            country_code="US"
            # Missing state_abbr and city
        )
        with self.assertRaises(ValidationError):
            location.full_clean()

class AccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = Location.objects.create(
            id="US-CA",
            title="California",
            center="POINT(-119.4179 36.7783)",
            location_type="state",
            country_code="US",
            state_abbr="CA",
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

    def test_accommodation_creation(self):
        """
        Test the creation of the Accommodation model.
        """
        self.assertEqual(Accommodation.objects.count(), 1)
        accommodation = Accommodation.objects.get(id="accommodation1")
        self.assertEqual(accommodation.title, "Beautiful House")
        self.assertEqual(accommodation.location.title, "California")

    def test_accommodation_str(self):
        """
        Test the string representation of the Accommodation model.
        """
        accommodation = Accommodation.objects.get(id="accommodation1")
        self.assertEqual(str(accommodation), "Beautiful House - California")

    def test_accommodation_invalid(self):
        """
        Test that creating an Accommodation without required fields raises a validation error.
        """
        with self.assertRaises(IntegrityError):
            Accommodation.objects.create(
                id="accommodation2",
                title="Another House",
                country_code="US",
                bedroom_count=2,
                review_score=3.5,
                usd_rate=100.00,
                center="POINT(-118.2437 34.0522)",
                # Missing location and user
            )

class LocalizeAccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.location = Location.objects.create(
            id="US-CA",
            title="California",
            center="POINT(-119.4179 36.7783)",
            location_type="state",
            country_code="US",
            state_abbr="CA",
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

    def test_localize_accommodation_creation(self):
        """
        Test the creation of the LocalizeAccommodation model.
        """
        self.assertEqual(LocalizeAccommodation.objects.count(), 1)
        localized_accommodation = LocalizeAccommodation.objects.get(accommodation=self.accommodation)
        self.assertEqual(localized_accommodation.language, "en")
        self.assertEqual(localized_accommodation.description, "A beautiful house in California")

    def test_localize_accommodation_unique_together(self):
        """
        Test the unique constraint on accommodation and language.
        """
        with self.assertRaises(IntegrityError):
            LocalizeAccommodation.objects.create(
                accommodation=self.accommodation,
                language="en",  # Duplicate language for the same accommodation
                description="Another description",
                policy={"pet_policy": "Pets allowed"}
            )

    def test_localize_accommodation_str(self):
        """
        Test the string representation of the LocalizeAccommodation model.
        """
        localized_accommodation = LocalizeAccommodation.objects.get(accommodation=self.accommodation)
        self.assertEqual(str(localized_accommodation), "Beautiful House - en")

class LocationModelTest(TestCase):
    def test_location_invalid(self):
        """
        Test that creating a Location without required fields raises a validation error.
        """
        location = Location(
            id="CA",
            title="California",
            center="POINT(-119.4179 36.7783)",
            location_type="state",
            country_code="US"
            # Missing state_abbr and city
        )
        try:
            location.full_clean()  # This will raise a ValidationError if there are validation issues
        except ValidationError as e:
            self.assertTrue('state_abbr' in e.message_dict)
            self.assertTrue('city' in e.message_dict)
