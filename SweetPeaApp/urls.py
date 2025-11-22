from django.urls import path
from . import views

urlpatterns = [
    # Custom Admin Portal
    path('portal/login/', views.portal_login, name='portal_login'),
    path('portal/logout/', views.portal_logout, name='portal_logout'),
    path('portal/', views.portal_dashboard, name='portal_dashboard'),

    # Testimonial Management in Portal
    path('portal/testimonials/', views.PortalTestimonialListView.as_view(), name='portal_testimonial_list'),
    path('portal/testimonials/new/', views.PortalTestimonialCreateView.as_view(), name='portal_testimonial_create'),
    path('portal/testimonials/<int:pk>/edit/', views.PortalTestimonialUpdateView.as_view(), name='portal_testimonial_edit'),
    path('portal/testimonials/<int:pk>/delete/', views.PortalTestimonialDeleteView.as_view(), name='portal_testimonial_delete'), 
]

