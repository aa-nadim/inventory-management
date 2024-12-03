# models.py

import os
import pytest
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from properties.models import (
    Location, 
    Accommodation, 
    AccommodationImage, 
    LocalizeAccommodation,
    validate_amenities,
    upload_accommodation_image
)

@pytest.mark.django_db
class TestLocationModel:
    def test_location_creation(self):
        # Test creating a location with minimal required fields
        location = Location.objects.create(
            id='US-NY-NYC',
            title='New York City',
            center=Point(-74.0060, 40.7128),
            location_type='city',
            country_code='US',
            state_abbr='NY',
            city='New York City'
        )
        
        assert location.id == 'US-NY-NYC'
        assert location.title == 'New York City'
        assert location.location_type == 'city'
        assert location.country_code == 'US'
        assert str(location) == 'New York City (city)'

    def test_location_hierarchy(self):
        # Test hierarchical location structure
        usa = Location.objects.create(
            id='US',
            title='United States',
            center=Point(-98.5795, 39.8283),
            location_type='country',
            country_code='US'
        )
        
        ny_state = Location.objects.create(
            id='US-NY',
            title='New York State',
            center=Point(-75.4252, 42.9538),
            location_type='state',
            country_code='US',
            parent=usa,
            state_abbr='NY'
        )
        
        assert ny_state.parent == usa
        assert list(usa.children.all()) == [ny_state]

@pytest.mark.django_db
class TestAccommodationModel:
    def setup_method(self):
        # Create a location for testing
        self.location = Location.objects.create(
            id='US-NY-NYC',
            title='New York City',
            center=Point(-74.0060, 40.7128),
            location_type='city',
            country_code='US',
            state_abbr='NY',
            city='New York City'
        )
        
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )

    def test_accommodation_creation(self):
        accommodation = Accommodation.objects.create(
            id='PROP001',
            feed=1,
            title='Luxury Apartment',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=250.00,
            center=Point(-74.0060, 40.7128),
            location=self.location,
            amenities=['WiFi', 'Kitchen', 'Balcony'],
            user=self.user,
            published=True
        )
        
        assert accommodation.title == 'Luxury Apartment'
        assert accommodation.amenities == ['WiFi', 'Kitchen', 'Balcony']
        assert str(accommodation) == 'Luxury Apartment - New York City'

    def test_accommodation_amenities_validation(self):
        # Test valid amenities
        accommodation = Accommodation(
            id='PROP002',
            feed=1,
            title='Test Apartment',
            country_code='US',
            bedroom_count=1,
            review_score=4.0,
            usd_rate=150.00,
            center=Point(-74.0060, 40.7128),
            location=self.location,
            amenities=['WiFi', 'Pool'],
            user=self.user
        )
        accommodation.full_clean()  # Should not raise validation error

        # Test invalid amenities
        with pytest.raises(ValidationError):
            validate_amenities(['A' * 101])  # Amenity too long
        
        with pytest.raises(ValidationError):
            validate_amenities([123])  # Non-string amenity

@pytest.mark.django_db
class TestAccommodationImage:
    def setup_method(self):
        # Create location and accommodation
        location = Location.objects.create(
            id='US-CA-SF',
            title='San Francisco',
            center=Point(-122.4194, 37.7749),
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco'
        )
        
        user = User.objects.create_user(
            username='imageuser', 
            password='testpass'
        )
        
        self.accommodation = Accommodation.objects.create(
            id='PROP003',
            feed=1,
            title='Test Accommodation',
            country_code='US',
            bedroom_count=1,
            review_score=4.5,
            usd_rate=200.00,
            center=Point(-122.4194, 37.7749),
            location=location,
            user=user
        )

    def test_upload_accommodation_image(self):
        # Create a test image
        test_image = SimpleUploadedFile(
            name='test_image.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        
        # Create accommodation image
        accommodation_image = AccommodationImage.objects.create(
            accommodation=self.accommodation,
            image=test_image
        )
        
        assert accommodation_image.accommodation == self.accommodation
        assert str(accommodation_image) == f"Image for {self.accommodation.title}"

    def test_upload_accommodation_image_path(self):
        # Test the custom upload path function
        filename = 'test_photo.jpg'
        path = upload_accommodation_image(
            type('obj', (), {'accommodation': self.accommodation}), 
            filename
        )
        
        assert path.startswith(f'accommodations/{self.accommodation.id}/images/')
        assert path.endswith('.jpg')

@pytest.mark.django_db
class TestLocalizeAccommodation:
    def setup_method(self):
        # Create location and accommodation
        location = Location.objects.create(
            id='US-TX-HOU',
            title='Houston',
            center=Point(-95.3698, 29.7604),
            location_type='city',
            country_code='US',
            state_abbr='TX',
            city='Houston'
        )
        
        user = User.objects.create_user(
            username='localizeuser', 
            password='testpass'
        )
        
        self.accommodation = Accommodation.objects.create(
            id='PROP004',
            feed=1,
            title='Localized Test Accommodation',
            country_code='US',
            bedroom_count=1,
            review_score=4.5,
            usd_rate=200.00,
            center=Point(-95.3698, 29.7604),
            location=location,
            user=user
        )

    def test_localize_accommodation(self):
        # Create localized version
        localized = LocalizeAccommodation.objects.create(
            accommodation=self.accommodation,
            language='en',
            description='Cozy apartment in downtown',
            policy={'cancellation': 'Flexible'}
        )
        
        assert localized.language == 'en'
        assert localized.description == 'Cozy apartment in downtown'
        assert localized.policy == {'cancellation': 'Flexible'}
        assert str(localized) == f"Localized Test Accommodation - en"

    def test_unique_language_constraint(self):
        # Create first localization
        LocalizeAccommodation.objects.create(
            accommodation=self.accommodation,
            language='en',
            description='English description'
        )
        
        # Attempt to create another with same language should raise exception
        with pytest.raises(Exception):
            LocalizeAccommodation.objects.create(
                accommodation=self.accommodation,
                language='en',
                description='Another English description'
            )


# admin.py

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from django.contrib.admin.sites import AdminSite
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal

from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation
from .admin import (
    LocationAdmin, 
    AccommodationAdmin, 
    AccommodationImageAdmin, 
    LocalizeAccommodationAdmin
)

class AdminTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.superuser = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='testpass123'
        )
        
        # Create a property owner group
        self.property_owners_group, _ = Group.objects.get_or_create(name='Property Owners')
        
        # Create a regular property owner user
        self.property_owner = User.objects.create_user(
            username='owner', 
            email='owner@example.com', 
            password='testpass123'
        )
        self.property_owner.groups.add(self.property_owners_group)
        
        # Create a location with a center point
        self.location = Location.objects.create(
            title='Test Location',
            location_type='city',
            country_code='US',
            state_abbr='CA',
            city='San Francisco',
            center=Point(-122.4194, 37.7749)  # San Francisco coordinates
        )
        
        # Create an accommodation with more complete data
        self.accommodation = Accommodation.objects.create(
            title='Test Accommodation',
            country_code='US',
            bedroom_count=2,
            review_score=4.5,
            usd_rate=Decimal('100.00'),
            location=self.location,
            published=True,
            user=self.property_owner,
            center=Point(-122.4194, 37.7749)  # Same coordinates as location
        )

    def test_location_creation(self):
        """
        Verify that Location is created correctly with center point
        """
        self.assertIsNotNone(self.location.center)
        self.assertEqual(self.location.center.x, -122.4194)
        self.assertEqual(self.location.center.y, 37.7749)

    def test_location_admin(self):
        """
        Test LocationAdmin functionality
        """
        admin_instance = LocationAdmin(Location, AdminSite())
        
        # Test list display
        self.assertEqual(
            list(admin_instance.get_list_display(None)), 
            ['id', 'title', 'location_type', 'country_code', 'state_abbr', 'city']
        )
        
        # Test search fields
        self.assertEqual(
            admin_instance.search_fields, 
            ('title', 'country_code', 'state_abbr', 'city')
        )
        
        # Test list filters
        self.assertEqual(
            admin_instance.list_filter, 
            ('location_type', 'country_code')
        )

    def test_accommodation_admin_queryset(self):
        """
        Test get_queryset method for property owner and superuser
        """
        # Create a request for property owner
        factory = RequestFactory()
        request_owner = factory.get('/')
        request_owner.user = self.property_owner
        
        # Create a request for superuser
        request_super = factory.get('/')
        request_super.user = self.superuser
        
        admin_instance = AccommodationAdmin(Accommodation, AdminSite())
        
        # Check queryset for property owner
        owner_qs = admin_instance.get_queryset(request_owner)
        self.assertEqual(list(owner_qs), [self.accommodation])
        
        # Check queryset for superuser
        super_qs = admin_instance.get_queryset(request_super)
        self.assertTrue(self.accommodation in super_qs)

    def test_accommodation_image_admin(self):
        """
        Test AccommodationImageAdmin functionality
        """
        # Create an accommodation image
        accommodation_image = AccommodationImage.objects.create(
            accommodation=self.accommodation,
            image='test_image.jpg'
        )
        
        admin_instance = AccommodationImageAdmin(AccommodationImage, AdminSite())
        
        # Test list display
        self.assertEqual(
            list(admin_instance.get_list_display(None)), 
            ['accommodation', 'image', 'uploaded_at']
        )
        
        # Test search fields
        self.assertEqual(
            admin_instance.search_fields, 
            ('accommodation__title',)
        )

    def test_localize_accommodation_admin(self):
        """
        Test LocalizeAccommodationAdmin functionality
        """
        # Create a localized accommodation
        localized_accommodation = LocalizeAccommodation.objects.create(
            accommodation=self.accommodation,
            language='es',
            description='Descripción de prueba'
        )
        
        admin_instance = LocalizeAccommodationAdmin(LocalizeAccommodation, AdminSite())
        
        # Test list display
        self.assertEqual(
            list(admin_instance.get_list_display(None)), 
            ['id', 'accommodation', 'language', 'description']
        )
        
        # Test list filters
        self.assertEqual(
            admin_instance.list_filter, 
            ('language',)
        )
        
        # Test search fields
        self.assertEqual(
            admin_instance.search_fields, 
            ('description', 'language')
        )


# urls.py
import pytest
from django.urls import reverse, resolve
from . import views

@pytest.mark.django_db
class TestUrlRouting:
    def test_home_url_resolves(self):
        """
        Test that the root URL resolves to the home view
        """
        url = reverse('home')
        assert url == '/'
        
        resolved_view = resolve('/')
        assert resolved_view.func == views.home

    def test_signup_url_resolves(self):
        """
        Test that the signup URL resolves correctly
        """
        url = reverse('signup')
        assert url == '/signup/'
        
        resolved_view = resolve('/signup/')
        assert resolved_view.func == views.signup

    def test_signup_success_url_resolves(self):
        """
        Test that the signup success URL resolves correctly
        """
        url = reverse('signup_success')
        assert url == '/signup/success/'
        
        resolved_view = resolve('/signup/success/')
        assert resolved_view.func == views.signup_success

    def test_url_names_are_unique(self):
        """
        Ensure each URL name is unique
        """
        url_names = ['home', 'signup', 'signup_success']
        assert len(set(url_names)) == len(url_names), "URL names must be unique"


