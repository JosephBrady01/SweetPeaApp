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

    # Services
    path("services/home-help/", views.home_help_view, name="service_home_help"),
    path("services/companionship/", views.companionship_view, name="service_companionship"),
    path("services/out-and-about/", views.out_and_about_view, name="service_out_and_about"),
    path("services/respite-care/", views.respite_care_view, name="service_respite_care"),
]

