from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# Model for testimonials: An admin should be able to create, update and delete a testimonial
class Testimonials(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    location = models.CharField(max_length=100, blank=True)
    reviewer = models.CharField(max_length=100, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    """
        Returns a human-readable representation of the testimonial.
        This is primarily used in the Django admin interface and debugging.
        """
    def __str__(self):
        return f"testimonial by {self.author.first_name} ({self.location or 'No Location'})" 
    
# Model for resources: An admin should be able to create, update and delete a resources
class ResourceDocument(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="resources/%Y/%m/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_resources",
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title