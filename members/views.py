from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import DetailView, CreateView 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from hamyon.models import Profile 
from django.contrib.auth.models import User

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = "registration/create_user_profile_page.html"
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
class EditProfilePageView(generic.UpdateView):
    model = Profile 
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'telegram_url']
    def get_success_url(self):
        profile_id=self.kwargs['pk']    
        return reverse_lazy('show_profile_page', kwargs={'pk': profile_id})

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
     
    def get_context_data(self, *args, **kwargs):
        #users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)        
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])      
        context["page_user"] = page_user
        return context

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    #form_class = PasswordChangeForm    
    success_url = reverse_lazy('password_success')
    #success_url = reverse_lazy('home')

def password_success(request):
    return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
class UserEditView(generic.UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    def get_success_url(self):
        profileid=self.kwargs['pk']    
        return reverse_lazy('show_profile_page', kwargs={'pk': profileid})

