from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Testimonials
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def home(request):
    """
    Renders the Sweet Pea homepage.
    For now, this can display static content or eventually include
    dynamic testimonials, blog posts, etc.
    """
    testimonials = Testimonials.objects.all()
    return render(request, 'SweetPeaApp/base.html', {'testimonials': testimonials})


def register(request):
    """
    Allows new users to register for an account.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

class TestimonialListView(ListView):
    """
    Displays testimonials on the website

    """
    model = Testimonials
    template_name = 'SweetPeaApp/testimonials/testimonial_list.html'
    context_object_name = 'testimonials'


class TestimonialCreateView(LoginRequiredMixin, CreateView):
    """
    Allows logged-in users to create a new testimonial

    """
    model = Testimonials
    fields = ['body']
    template_name = 'SweetPeaApp/testimonials/testimonial_form.html'
    success_url = reverse_lazy('testimonial_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class TestimonialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allows a logged-in user to update testimonials

    """
    model = Testimonials
    fields = ['body']
    template_name = 'SweetPeaApp/testimonials/testimonial_form.html'
    success_url = reverse_lazy('testimonial_list')

    def test_func(self):
        testimonial = self.get_object()
        return testimonial.author == self.request.user
    
class TestimonialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allows a logged-in user to delete a testimonial

    """
    model = Testimonials
    template_name = 'SweetPeaApp/testimonials/testimonial_confirm_delete.html'
    success_url = reverse_lazy('testimonial_list')

    def test_func(self):
        testimonial = self.get_object()
        return testimonial.author == self.request.user
    
# ------------------------------
# 🔐 CUSTOM ADMIN PORTAL VIEWS
# ------------------------------


# Utility: restrict portal access to staff or superusers
def staff_check(user):
    return user.is_staff or user.is_superuser


# ------------------------------
# 🔸 LOGIN / LOGOUT
# ------------------------------

def portal_login(request):
    """
    Custom login page for Sweet Pea Admin Portal.
    Only staff/superusers can log in.
    """
    if request.user.is_authenticated:
        return redirect('portal_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user and staff_check(user):
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('portal_dashboard')
        else:
            messages.error(request, "Invalid credentials or insufficient permissions.")

    return render(request, 'SweetPeaApp/portal/admin_login.html')


@login_required
def portal_logout(request):
    """
    Logs out the current user and redirects to the portal login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('portal_login')


# ------------------------------
# 🏠 DASHBOARD
# ------------------------------

@login_required
@user_passes_test(staff_check)
def portal_dashboard(request):
    """
    Displays the admin dashboard for staff/superusers.
    Shows quick stats and navigation cards.
    """
    testimonial_count = Testimonials.objects.count()
    user = request.user

    return render(request, 'SweetPeaApp/portal/dashboard.html', {
        'testimonial_count': testimonial_count,
        'user': user,
    })


# ------------------------------
# 💬 TESTIMONIAL MANAGEMENT (PORTAL)
# ------------------------------

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Restricts access to logged-in staff or superusers.
    Used by all portal CRUD views.
    """
    def test_func(self):
        return staff_check(self.request.user)


class PortalTestimonialListView(StaffRequiredMixin, ListView):
    """
    Displays all testimonials in the admin portal for management.
    """
    model = Testimonials
    template_name = 'SweetPeaApp/portal/admin_testimonial_list.html'
    context_object_name = 'testimonials'
    ordering = ['-created_at']


class PortalTestimonialCreateView(StaffRequiredMixin, CreateView):
    """
    Allows staff/superusers to create a new testimonial via the portal.
    """
    model = Testimonials
    fields = ['body']
    template_name = 'SweetPeaApp/portal/testimonial_form.html'
    success_url = reverse_lazy('portal_testimonial_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "✅ Testimonial added successfully.")
        return super().form_valid(form)


class PortalTestimonialUpdateView(StaffRequiredMixin, UpdateView):
    """
    Allows editing of existing testimonials via the portal.
    """
    model = Testimonials
    fields = ['body']
    template_name = 'SweetPeaApp/portal/testimonial_form.html'
    success_url = reverse_lazy('portal_testimonial_list')

    def form_valid(self, form):
        messages.success(self.request, "✏️ Testimonial updated successfully.")
        return super().form_valid(form)


class PortalTestimonialDeleteView(StaffRequiredMixin, DeleteView):
    """
    Allows deletion of testimonials via the portal.
    """
    model = Testimonials
    template_name = 'SweetPeaApp/portal/testimonial_confirm_delete.html'
    success_url = reverse_lazy('portal_testimonial_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Testimonial deleted successfully.")
        return super().delete(request, *args, **kwargs)

