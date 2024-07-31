# admin.py

from django.contrib import admin
from .models import GeneratedImage


@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the GeneratedImage model.
    """
    # Columns to display in the list view of the admin interface
    list_display = ('prompt', 'created_at', 'image_preview')

    # Filters to add on the list view sidebar
    list_filter = ('created_at',)

    # Fields to search within the admin interface
    search_fields = ('prompt',)

    # Fields to be displayed as readonly
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """
        Returns the URL of the image for display in the admin list view.

        Args:
            obj (GeneratedImage): The instance of the GeneratedImage model.

        Returns:
            str: The URL of the image or 'No Image' if no image is set.
        """
        return obj.image.url if obj.image else 'No Image'

    image_preview.short_description = 'Image URL'

    # Short description for the 'image_preview' field in the admin interface

    def view_image(self, obj):
        """
        Provides an HTML snippet to render the image in the admin detail view.

        Args:
            obj (GeneratedImage): The instance of the GeneratedImage model.

        Returns:
            str: HTML snippet to render the image preview.
        """
        return f'<img src="{obj.image.url}" width="300" height="300" />'

    view_image.short_description = 'Image Preview'
    view_image.allow_tags = True
    # Allow HTML tags in the admin interface for 'view_image' field

    # Define the fields to be displayed in the detail view of the admin interface
    fields = ('prompt', 'image', 'created_at', 'view_image')

    # Define fields as readonly in the detail view
    readonly_fields = ('created_at', 'view_image')
