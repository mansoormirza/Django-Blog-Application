from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('blog-home'))  # Redirect to profile page if already logged in
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #inserting data POSTED from the form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') #validated form data will be in the cleaned_data dictionary
            messages.success(request, f'Your account has been created, you can now log in!')
            return redirect ('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect ('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')