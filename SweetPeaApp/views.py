from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Testimonials
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, TestimonialForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import FileResponse, Http404
from django.utils.text import slugify
from .forms import ResourceDocumentForm
from .models import ResourceDocument
from django.shortcuts import render


# Create your views here.

def home(request):
    """
    Renders the Sweet Pea homepage.
    For now, this can display static content or eventually include
    dynamic testimonials, blog posts, etc.
    """
    testimonials = Testimonials.objects.all()
    return render(request, 'SweetPeaApp/base.html', {'testimonials': testimonials})

def privacy(request):
    return render(request, "SweetPeaApp/privacy.html")

def cookies(request):
    return render(request, "SweetPeaApp/cookies.html")


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
    fields = ['body', 'location', 'reviewer']
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
    fields = ['body', 'location', 'reviewer']
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
    
def home_help_view(request):
    return render(request, "SweetPeaApp/services/home_help.html")

def companionship_view(request):
    return render(request, "SweetPeaApp/services/companionship.html")

def out_and_about_view(request):
    return render(request, "SweetPeaApp/services/out_and_about.html")

def respite_care_view(request):
    return render(request, "SweetPeaApp/services/respite_care.html")
    
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
    resources_count = ResourceDocument.objects.count()
    user = request.user

    return render(request, 'SweetPeaApp/portal/dashboard.html', {
        'testimonial_count': testimonial_count,
        'resources_count': resources_count,
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
    form_class = TestimonialForm   # 👈 use the form, not fields
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
    form_class = TestimonialForm   # 👈 keep form consistent
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
    
# ------------------------------
# 📁 RESOURCE DOCUMENT MANAGEMENT
# ------------------------------

@login_required
@user_passes_test(staff_check)
def resources_list(request):
    docs = ResourceDocument.objects.all().order_by("-created_at")
    return render(request, "SweetPeaApp/portal/resources_list.html", {"docs": docs})


@login_required
def resource_upload(request):
    if request.method == "POST":
        form = ResourceDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            return redirect("resources_list")
    else:
        form = ResourceDocumentForm()
    return render(request, "SweetPeaApp/portal/resources_upload.html", {"form": form})

# app/views.py (add)
from django.shortcuts import get_object_or_404

def resource_download(request, pk: int):
    doc = get_object_or_404(ResourceDocument, pk=pk, is_published=True)

    if not doc.file or not doc.file.storage.exists(doc.file.name):
        raise Http404("File missing")

    # FileResponse streams efficiently
    response = FileResponse(doc.file.open("rb"), as_attachment=True)

    # Optional: nicer filename
    safe_title = slugify(doc.title) or "resource"
    original_ext = doc.file.name.split(".")[-1].lower()
    response["Content-Disposition"] = f'attachment; filename="{safe_title}.{original_ext}"'
    return response

class PortalResourceUpdateView(StaffRequiredMixin, UpdateView):
    model = ResourceDocument
    form_class = ResourceDocumentForm
    template_name = "SweetPeaApp/portal/resources_upload.html"  # reuse your form template
    success_url = reverse_lazy("resources_list")

    def form_valid(self, form):
        messages.success(self.request, "✏️ Resource updated successfully.")
        return super().form_valid(form)


class PortalResourceDeleteView(StaffRequiredMixin, DeleteView):
    model = ResourceDocument
    template_name = "SweetPeaApp/portal/resources_confirm_delete.html"
    success_url = reverse_lazy("resources_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Resource deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.utils.text import slugify

from .models import ResourceDocument


def public_resources(request):
    docs = ResourceDocument.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "SweetPeaApp/resources.html", {"docs": docs})


def public_resource_download(request, pk: int):
    doc = get_object_or_404(ResourceDocument, pk=pk, is_published=True)

    if not doc.file:
        raise Http404("No file attached")

    response = FileResponse(doc.file.open("rb"), as_attachment=True)

    # Optional: nice filename
    safe_title = slugify(doc.title) or "resource"
    ext = doc.file.name.split(".")[-1].lower()
    response["Content-Disposition"] = f'attachment; filename="{safe_title}.{ext}"'
    return response


