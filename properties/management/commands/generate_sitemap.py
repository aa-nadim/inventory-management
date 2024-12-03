import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from properties.models import Location
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Generates a sitemap.json file for country, state, and city locations'

    def handle(self, *args, **kwargs):
        # Fetch all country locations
        countries = Location.objects.filter(location_type='country').order_by('title')

        sitemap_data = []

        for country in countries:
            country_slug = slugify(country.title)
            locations = []

            # Fetch locations for the country (states)
            sub_locations = Location.objects.filter(parent=country).order_by('title')

            for location in sub_locations:
                location_slug = slugify(location.title)
                location_entry = {
                    location.title: location_slug
                }
                
                # Check if it's a state and fetch cities under it
                if location.location_type == 'state':
                    # Initialize a list for cities within this state
                    cities_list = []
                    cities = Location.objects.filter(parent=location).order_by('title')
                    
                    for city in cities:
                        city_slug = slugify(city.title)
                        cities_list.append({
                            city.title: f"{country_slug}/{location_slug}/{city_slug}"
                        })

                    # Add cities to the state entry if there are any
                    if cities_list:
                        location_entry['locations'] = cities_list

                locations.append(location_entry)

            # Append country with its locations (states and cities)
            sitemap_data.append({
                country.title: country_slug,
                'locations': locations
            })

        # Sort the sitemap data by country title (alphabetically)
        sitemap_data = sorted(sitemap_data, key=lambda x: list(x.keys())[0].lower())

        # Output the JSON data to a file
        output_path = os.path.join(settings.BASE_DIR, 'sitemap.json')
        with open(output_path, 'w') as f:
            json.dump(sitemap_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Sitemap generated successfully at {output_path}"))