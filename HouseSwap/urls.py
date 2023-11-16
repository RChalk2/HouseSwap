"""
URL configuration for HouseSwap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfig 
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # include Django built in admin urls
    path("admin/", admin.site.urls),
    # Include the URLs of the kswap app
    path("", include("kswap.urls")),
    # Include urls for login, logout and password management
    path("", include("users.urls")),
]


# The four lines below are from:
# https://medium.com/@biswajitpanda973/creating-a-dynamic-product-gallery-in-django-a-guide-to-multi-image-uploads-1cefdb418201
# It adds a url to be used for serving media files
# It uses the static function
# settings.MEDIA_URL is set to  "/media/" in settings.py
# settings.MEDIA_ROOT is set to os.path.join(BASE_DIR, "media") in settings.py
# so this code tells django that the url /media should serve images in /media/images
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # I will use Django  to serve my pictures even in production
    # This is not recommended - it seems I should really set up  some other
    # kind of  server for this
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)