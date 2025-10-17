from django.contrib import admin
from .models import Testimonials

# Register your models here.

@admin.register(Testimonials)
class TestimonialAdmin(admin.ModelAdmin):
    """
    Customises how testimonials appear in the built-in admin interface

    """
    list_display = ('author', 'short_body', 'created_at', 'updated_at')
    search_fields = ('body', 'author_firstname')

    def short_body(self, obj):
        """
        Returns a shortened preview of the text for the admin list

        """
        return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body
    short_body.short_description = "Testimonial"
