from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation
from import_export.admin import ImportExportModelAdmin
from .resources import LocationResource

@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ('id', 'title', 'location_type', 'country_code', 'parent', 'created_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')

class AccommodationImageInline(admin.TabularInline):
    """
    Inline admin for managing images related to an Accommodation.
    """
    model = AccommodationImage
    extra = 1  # Number of empty slots to display for adding new images
    fields = ('image',)  # Fields to display in the inline
    readonly_fields = ('uploaded_at',)

@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'center', 'location', 'published', 'created_at', 'updated_at')
    list_filter = ('published', 'location')
    search_fields = ('title', 'country_code', 'location__title')
    ordering = ('-created_at',)
    inlines = [AccommodationImageInline]

    settings_overrides = {
        'DEFAULT_CENTER': (0, 0),
        'DEFAULT_ZOOM': 6,
    }

    def get_queryset(self, request):
        """
        Limit queryset to show only accommodations created by the logged-in user for Property Owners,
        but allow superusers to see all accommodations.
        """
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.groups.filter(name='Property Owners').exists():
            return qs.filter(user_id=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        """
        Automatically assign the logged-in user as the creator if not set.
        """
        if not obj.user_id:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        """
        Allow Property Owner users to edit only their own accommodations,
        but allow superusers to edit any accommodation.
        """
        if request.user.is_superuser:
            return True
        if obj and obj.user_id != request.user:
            return False
        return super().has_change_permission(request, obj)
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Limit the user field dropdown to only show the current user or allow superusers to select any user.
        """
        form = super().get_form(request, obj, **kwargs)

        # If the user is not a superuser, set the user field to the current user and disable the dropdown
        if not request.user.is_superuser:
            form.base_fields['user'].initial = request.user  # Pre-set the user to the current logged-in user
            form.base_fields['user'].disabled = True  # Disable the dropdown to prevent changes

        return form

    def has_delete_permission(self, request, obj=None):
        """
        Allow Property Owner users to delete only their own accommodations,
        but allow superusers to delete any accommodation.
        """
        if request.user.is_superuser:
            return True
        if obj and obj.user_id != request.user:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(AccommodationImage)
class AccommodationImageAdmin(admin.ModelAdmin):
    """
    Admin interface for the AccommodationImage model.
    """
    list_display = ('accommodation', 'image', 'uploaded_at')
    search_fields = ('accommodation__title',)

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'accommodation', 'language', 'description')
    list_filter = ('language',)
    search_fields = ('description', 'language')
