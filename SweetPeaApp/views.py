from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Testimonials
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


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
