from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Model for testimonials: An admin should be able to create, update and delete a testimonial
class Testimonials(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    location = models.CharField(max_length=100, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    """
        Returns a human-readable representation of the testimonial.
        This is primarily used in the Django admin interface and debugging.
        """
    def __str__(self):
        return f"testimonial by {self.author.first_name} ({self.location or 'No Location'})" 