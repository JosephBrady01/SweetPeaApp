from django.urls import path
from . import views

urlpatterns = [
    path('', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('new/', views.TestimonialCreateView.as_view(), name='testimonial_create'),
    path('<int:pk>/edit/', views.TestimonialUpdateView.as_view(), name='testimonial_edit'),
    path('<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),

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

