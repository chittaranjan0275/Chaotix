from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the image generation view
    # This pattern matches the URL /generate/ and maps it to the generate_images_in_parallel view
    # The name 'generate_images' can be used to refer to this URL pattern in templates and other parts of the code
    path('generate/', views.generate_images_in_parallel, name='generate_images'),

    # URL pattern for viewing the output of image generation tasks
    # This pattern matches the URL /output/<task_ids>/ where <task_ids> is a string representing task IDs
    # It maps to the image_output view and allows passing task IDs as a parameter
    # The name 'image_output' can be used to refer to this URL pattern
    path('output/<str:task_ids>/', views.image_output, name='image_output'),

    # URL pattern for listing all generated images
    # This pattern matches the URL /images/ and maps it to the image_list view
    # The name 'image_list' can be used to refer to this URL pattern
    path('images/', views.image_list, name='image_list'),

    # URL pattern for viewing details of a specific image
    # This pattern matches the URL /images/<image_id>/ where <image_id> is an integer representing the image ID
    # It maps to the image_detail view and allows passing the image ID as a parameter
    # The name 'image_detail' can be used to refer to this URL pattern
    path('images/<int:image_id>/', views.image_detail, name='image_detail'),
]
