"""
URL configuration for SweetPeaProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
"""
URL configuration for SweetPeaProject project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Sitemap framework: serves the XML sitemap at /sitemap.xml
from django.contrib.sitemaps.views import sitemap

# Project views and the sitemap class we just created
from SweetPeaApp import views
from SweetPeaApp.sitemaps import StaticViewSitemap

# Map sitemap section names to their classes. Django expects a dict here even
# if there's only one section. We can add more later (e.g. for blog posts).
sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path("resources/", views.public_resources, name="public_resources"),
    path("resources/<int:pk>/download/", views.public_resource_download, name="public_resource_download"),
    path('admin/', admin.site.urls),

    # Homepage
    path('', views.home, name='home'),

    # Sitemap endpoint - Google fetches this to discover the site's URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

    path('', include('SweetPeaApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
