from import_export import resources
from .models import Location

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        import_id_fields = ['id']  # Use 'id' as the unique identifier for imports
        fields = (
            'id',
            'title',
            'center',
            'parent',
            'location_type',
            'country_code',
            'state_abbr',
            'city',
            'created_at',
            'updated_at',
        )  # Specify the fields to import/export
