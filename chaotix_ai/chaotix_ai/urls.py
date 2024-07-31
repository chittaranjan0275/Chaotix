"""chaotix_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Include URLs from the 'image_generator' app
    path('', include('image_generator.urls')),
]

if settings.DEBUG:
    """
    Serve media files during development.

    In a production environment, media files should be served by a web server
    or a cloud storage service, not Django itself.
    """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
