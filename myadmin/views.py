from django.shortcuts import render, redirect
from django.contrib import messages

from account.models import CustomUser
from . import forms

def admin_dashboard(request):
    users_list = CustomUser.objects.filter(is_active=True)

    context = {'users_list':users_list}
    return render(request, 'myadmin/admin_dashboard.html', context)


def register_user_view(request):
    form = forms.CustomUserCreationForm(request.POST or None)
    profile_form = forms.ProfileCreationForm(request.POST or None, request.FILES or None)

    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        user_profile = profile_form.save(commit=False)
        user_profile.user = user
        user_profile.save()
        messages.success(request, 'New account is registered successfully')
        return redirect('myadmin:register_user')

    context = {'form':form, 'profile_form':profile_form}
    return render(request, 'myadmin/register.html', context)
