import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from decimal import Decimal
import os
from unittest.mock import Mock, patch
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
    """Fixture to create a sample Location instance."""
    return Location.objects.create(
        id='US-NY-NYC',
        title='New York City',
        center=Point(-74.0060, 40.7128),
        location_type='city',
        country_code='US',
        state_abbr='NY',
        city='New York'
    )

@pytest.fixture
def sample_user():
    """Fixture to create a sample User instance."""
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def sample_accommodation(sample_location, sample_user):
    """Fixture to create a sample Accommodation instance."""
    return Accommodation.objects.create(
        id='ACC001',
        feed=1,
        title='Cozy Apartment',
        country_code='US',
        bedroom_count=2,
        review_score=4.5,
        usd_rate=Decimal('150.00'),
        center=Point(-74.0060, 40.7128),
        location=sample_location,
        user=sample_user,
        amenities=['WiFi', 'Kitchen'],
        published=True
    )

@pytest.mark.django_db
def test_location_creation(sample_location):
    """Test Location model creation and string representation."""
    assert sample_location.title == 'New York City'
    assert sample_location.location_type == 'city'
    assert str(sample_location) == 'New York City (city)'

@pytest.mark.django_db
def test_location_hierarchy(sample_location):
    """Test location hierarchical structure."""
    child_location = Location.objects.create(
        id='US-NY-BK',
        title='Brooklyn',
        center=Point(-73.9442, 40.6782),
        parent=sample_location,
        location_type='city',
        country_code='US',
        state_abbr='NY'
    )
    
    assert child_location.parent == sample_location
    assert list(sample_location.children.all()) == [child_location]

@pytest.mark.django_db
def test_accommodation_creation(sample_accommodation):
    """Test Accommodation model creation."""
    assert sample_accommodation.title == 'Cozy Apartment'
    assert sample_accommodation.bedroom_count == 2
    assert sample_accommodation.review_score == Decimal('4.5')
    assert str(sample_accommodation) == 'Cozy Apartment - New York City'

def test_validate_amenities():
    """Test custom amenities validator."""
    # Valid case
    validate_amenities(['WiFi', 'Kitchen'])
    
    # Invalid cases
    with pytest.raises(ValidationError):
        validate_amenities('Not a list')
    
    with pytest.raises(ValidationError):
        validate_amenities([123, 'Kitchen'])
    
    with pytest.raises(ValidationError):
        validate_amenities(['A' * 101])

@pytest.mark.django_db
def test_accommodation_image_upload(sample_accommodation):
    """Test AccommodationImage upload functionality."""
    # Mock file for upload
    mock_file = Mock()
    mock_file.name = 'test_image.jpg'
    
    image = AccommodationImage.objects.create(
        accommodation=sample_accommodation,
        image=mock_file
    )
    
    assert image.accommodation == sample_accommodation
    assert str(image) == f"Image for {sample_accommodation.title}"

@pytest.mark.django_db
def test_localize_accommodation(sample_accommodation):
    """Test LocalizeAccommodation model."""
    localized = LocalizeAccommodation.objects.create(
        accommodation=sample_accommodation,
        language='es',
        description='Apartamento acogedor',
        policy={'check_in': '14:00', 'check_out': '11:00'}
    )
    
    assert localized.language == 'es'
    assert str(localized) == 'Cozy Apartment - es'

@pytest.mark.django_db
def test_upload_accommodation_image_path(sample_accommodation):
    """Test custom upload path for accommodation images."""
    mock_instance = Mock()
    mock_instance.accommodation = sample_accommodation
    
    filename = 'test image.jpg'
    result_path = upload_accommodation_image(mock_instance, filename)
    
    assert result_path.startswith(f'accommodations/{sample_accommodation.id}/images/')
    assert 'test-image' in result_path
    assert result_path.endswith('.jpg')

@pytest.mark.django_db
def test_accommodation_publication_status(sample_accommodation):
    """Test accommodation publication status."""
    assert sample_accommodation.published is True
    
    sample_accommodation.published = False
    sample_accommodation.save()
    
    refreshed_accommodation = Accommodation.objects.get(id=sample_accommodation.id)
    assert refreshed_accommodation.published is False

@pytest.mark.django_db
def test_accommodation_with_empty_amenities(sample_location, sample_user):
    """Test accommodation creation with empty amenities."""
    accommodation = Accommodation.objects.create(
        id='ACC002',
        feed=2,
        title='Empty Amenities Apartment',
        country_code='US',
        bedroom_count=1,
        review_score=4.0,
        usd_rate=Decimal('100.00'),
        center=Point(-74.0060, 40.7128),
        location=sample_location,
        user=sample_user,
        amenities=None,
        published=True
    )
    
    assert accommodation.amenities is None