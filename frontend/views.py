from django.shortcuts import render, redirect
from django.contrib import messages

from myadmin import forms

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('myadmin:admin_dashboard')
        else:
            return redirect('account:customer_dashboard')
    return render(request, 'frontend/index.html')



def signup_user_view(request):
    form = forms.CustomUserCreationForm(request.POST or None)
    profile_form = forms.ProfileCreationForm(request.POST or None, request.FILES or None)

    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        user_profile = profile_form.save(commit=False)
        user_profile.user = user
        user_profile.save()
        messages.success(request, 'New account is registered successfully')
        return redirect('frontend:sign_up')

    context = {'form':form, 'profile_form':profile_form}
    return render(request, 'frontend/signup.html', context)