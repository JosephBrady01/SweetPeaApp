# Sitemap definitions for sweetpeahomehelp.co.uk
# Tells search engines which public URLs exist and roughly how important each one is.
# The Django admin and the /portal/ admin dashboard are deliberately excluded.

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """
    Sitemap for public, static pages — pages that aren't generated from database content.
    Each entry is a URL name from the project's url configuration.
    """

    # How often Google should expect content on these pages to change.
    # 'monthly' is sensible for a small business site that rarely updates.
    changefreq = 'monthly'

    # Default priority (overridden per-URL in the priority() method below).
    priority = 0.5

    # Always serve sitemap URLs as HTTPS so Google indexes the canonical version.
    protocol = 'https'

    def items(self):
        # Return the URL name of every public page we want indexed.
        # Portal / admin / file-download routes are deliberately not included here.
        return [
            'home',
            'service_home_help',
            'service_companionship',
            'service_respite_care',
            'service_out_and_about',
            'public_resources',
            'privacy',
            'cookies',
        ]

    def location(self, item):
        # Convert each URL name into its actual URL path
        return reverse(item)

    def priority(self, item):
        # Relative importance of pages within the site (0.0 - 1.0).
        # Used by Google to understand which pages matter most.
        if item == 'home':
            return 1.0
        if item.startswith('service_'):
            return 0.8
        if item == 'public_resources':
            return 0.7
        if item in ('privacy', 'cookies'):
            return 0.3
        return 0.5