import os
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from decimal import Decimal
from unittest.mock import patch

from properties.models import (
    Location, 
    Accommodation, 
    AccommodationImage, 
    LocalizeAccommodation,
    validate_amenities,
    upload_accommodation_image
)

@pytest.fixture
def sample_location():
    """Create a sample Location instance for testing."""
    return Location.objects.create(
        id='US_NY_NYC',
        title='New York City',
        center=Point(-74.0060, 40.7128),
        location_type='city',
        country_code='US',
        state_abbr='NY',
        city='New York City'
    )

@pytest.fixture
def sample_user():
    """Create a sample User instance for testing."""
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def sample_accommodation(sample_location, sample_user):
    """Create a sample Accommodation instance for testing."""
    return Accommodation.objects.create(
        id='PROP123',
        feed=1,
        title='Luxury Apartment',
        country_code='US',
        bedroom_count=2,
        review_score=4.5,
        usd_rate=250.00,
        center=Point(-74.0060, 40.7128),
        location=sample_location,
        user=sample_user,
        amenities=['WiFi', 'Kitchen'],
        published=True
    )

@pytest.mark.django_db
def test_location_model(sample_location):
    """Test Location model creation and string representation."""
    assert str(sample_location) == 'New York City (city)'
    assert sample_location.parent is None
    assert sample_location.location_type == 'city'
    assert sample_location.country_code == 'US'

def test_validate_amenities():
    """Test the custom amenities validator."""
    # Valid cases
    validate_amenities(['WiFi', 'Kitchen'])

    # Invalid cases
    with pytest.raises(ValidationError, match="Amenities must be a list of strings."):
        validate_amenities("not a list")

    with pytest.raises(ValidationError, match="'123' is not a string."):
        validate_amenities([123])

    with pytest.raises(ValidationError, match="exceeds 100 characters"):
        validate_amenities(['A' * 101])

@pytest.mark.django_db
def test_accommodation_model(sample_accommodation):
    """Test Accommodation model creation and constraints."""
    assert str(sample_accommodation) == 'Luxury Apartment - New York City'
    assert sample_accommodation.bedroom_count == 2
    assert sample_accommodation.review_score == Decimal('4.5')
    assert sample_accommodation.amenities == ['WiFi', 'Kitchen']


@pytest.mark.django_db
def test_localize_accommodation(sample_accommodation):
    """Test LocalizeAccommodation model creation and language detection."""
    localized = LocalizeAccommodation.objects.create(
        accommodation=sample_accommodation,
        language='en',
        description='A beautiful luxury apartment in the heart of New York City.',
        policy={'check_in': '14:00', 'check_out': '11:00'}
    )

    assert str(localized) == 'Luxury Apartment - en'
    assert localized.language == 'en'

@pytest.mark.django_db
def test_location_hierarchy(sample_location):
    """Test location hierarchy with parent-child relationships."""
    child_location = Location.objects.create(
        id='US_NY_BROOKLYN',
        title='Brooklyn',
        center=Point(-73.9442, 40.6782),
        parent=sample_location,
        location_type='city',
        country_code='US',
        state_abbr='NY',
        city='Brooklyn'
    )

    assert child_location.parent == sample_location
    assert list(sample_location.children.all()) == [child_location]

@pytest.mark.django_db
def test_model_creation_and_save(sample_location, sample_user, sample_accommodation):
    """Comprehensive test to ensure all models can be created and saved."""
    # Verify each model can be saved successfully
    assert Location.objects.count() == 1
    assert User.objects.count() == 1
    assert Accommodation.objects.count() == 1
    
    # Create an accommodation image
    image = AccommodationImage.objects.create(
        accommodation=sample_accommodation,
        image='path/to/test/image.jpg'
    )
    assert AccommodationImage.objects.count() == 1
    
    # Create a localized accommodation
    LocalizeAccommodation.objects.create(
        accommodation=sample_accommodation,
        language='fr',
        description='Un appartement de luxe à New York.'
    )
    assert LocalizeAccommodation.objects.count() == 1

# Configuration for pytest
def pytest_configure(config):
    """Configure pytest settings."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'




# view.py
import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.test import Client
from django.contrib.messages import get_messages
from unittest.mock import patch
import logging

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def signup_form_data():
    """Fixture providing valid signup form data."""
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'TestPassword123!',
        'password2': 'TestPassword123!'
    }

@pytest.mark.django_db
def test_home_view(client):
    """
    Test the home view returns a 200 status code 
    and correct content.
    """
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert response.content == b"Welcome to the Home Page!"

@pytest.mark.django_db
def test_signup_view_get(client):
    """
    Test GET request to signup view.
    """
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_signup_view_invalid_form(client):
    """
    Test signup with invalid form data.
    """
    # Intentionally provide mismatched passwords
    invalid_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password1': 'TestPassword123!',
        'password2': 'DifferentPassword456!'
    }
    
    response = client.post(reverse('signup'), invalid_data)
    
    # Should remain on the signup page
    assert response.status_code == 200
    
    # Check that no user was created
    assert User.objects.count() == 0
    
    # Verify error messages
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0
    assert messages[0].tags == 'error'

# Configurable settings for pytest
def pytest_configure(config):
    """Configure pytest settings."""
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project.settings'