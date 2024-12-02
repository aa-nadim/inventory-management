from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, AccommodationImage, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city')
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
    inlines = [AccommodationImageInline]  # Add the inline for managing images
    
    # settings_overrides = {  # Optional: Customize Leaflet map settings
    #     'DEFAULT_CENTER': (0, 0),  # Latitude and Longitude for default map center
    #     'DEFAULT_ZOOM': 6,         # Default zoom level
    # }

    def get_queryset(self, request):
        """Limit queryset to show only accommodations created by the logged-in user for Property Owners."""
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            # Show only the accommodations created by the logged-in user
            return qs.filter(user_id=request.user)
        return qs  # Admins can see all accommodations

    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in user as the creator if not set."""
        if not obj.user_id:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        """Allow Property Owner users to edit only their own accommodations."""
        if obj and obj.user_id != request.user:
            return False  # Restrict Property Owners from editing others' records
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Allow Property Owner users to delete only their own accommodations."""
        if obj and obj.user_id != request.user:
            return False  # Restrict Property Owners from deleting others' records
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








# # class AccommodationAdmin(LeafletGeoAdmin):
#     list_display = ('id', 'title', 'country_code', 'usd_rate', 'review_score', 'bedroom_count', 'published', 'created_at', 'updated_at')
#     search_fields = ('title', 'country_code', 'location_id__title', 'amenities')
#     list_filter = ('published', 'location_id')
#     raw_id_fields = ('location_id', 'user_id')
#     ordering = ('-created_at',)

#     settings_overrides = {  # Optional: Customize Leaflet map settings
#         'DEFAULT_CENTER': (0, 0),  # Latitude and Longitude for default map center
#         'DEFAULT_ZOOM': 6,         # Default zoom level
#     }

#     def get_queryset(self, request):
#         """Limit queryset to show only accommodations created by the logged-in user for Property Owners."""
#         qs = super().get_queryset(request)
#         if request.user.groups.filter(name='Property Owners').exists():
#             # Show only the accommodations created by the logged-in user
#             return qs.filter(user_id=request.user)
#         return qs  # Admins can see all accommodations

#     def save_model(self, request, obj, form, change):
#         """Automatically assign the logged-in user as the creator if not set."""
#         if not obj.user_id:
#             obj.user_id = request.user
#         super().save_model(request, obj, form, change)

#     def has_change_permission(self, request, obj=None):
#         """Allow Property Owner users to edit only their own accommodations."""
#         if obj and obj.user_id != request.user:
#             return False  # Restrict Property Owners from editing others' records
#         return super().has_change_permission(request, obj)

#     def has_delete_permission(self, request, obj=None):
#         """Allow Property Owner users to delete only their own accommodations."""
#         if obj and obj.user_id != request.user:
#             return False  # Restrict Property Owners from deleting others' records
#         return super().has_delete_permission(request, obj)