from django.shortcuts import render
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.contrib.auth import get_user_model, login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm



class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('newas_list') 

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
# Create your views here.
