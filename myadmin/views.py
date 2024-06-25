from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import staff_required

from account.models import CustomUser, Profile, BankAccount
from . import forms
from stock.models import Stock, BuyStock


@login_required
@staff_required
def admin_dashboard(request):
    users_list = CustomUser.objects.filter(is_active=True, is_staff=False)

    context = {'users_list':users_list}
    return render(request, 'myadmin/admin_dashboard.html', context)


@login_required
@staff_required
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


@login_required
@staff_required
def edit_user_view(request, pk):
    user = CustomUser.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    form = forms.CustomUserEditForm(request.POST or None,instance=user)
    profile_form = forms.ProfileCreationForm(request.POST or None, request.FILES or None,instance=profile)

    if form.is_valid() and profile_form.is_valid():
        form.save()
        profile_form.save()
        messages.success(request, 'Account is updated successfully')
        return redirect('myadmin:admin_dashboard')

    context = {'form':form, 'profile_form':profile_form, 'profile':profile}
    return render(request, 'myadmin/edit_user.html', context)


@login_required
@staff_required
def detail_user_view(request, pk):
    user = CustomUser.objects.get(pk=pk)
    profile = Profile.objects.get(user=user)
    bank_account = BankAccount.objects.filter(user=user)
    user_stocks = BuyStock.objects.filter(user=user)

    context = {'user':user, 'profile':profile, 'bank_account':bank_account,
            'user_stocks':user_stocks}
    return render(request, 'myadmin/user_detail.html', context)


@login_required
@staff_required
def delete_user_view(request, pk):
    user = CustomUser.objects.get(pk=pk)
    user.delete()
    messages.success(request, 'User is deleted successfully')
    return redirect('myadmin:admin_dashboard')


@login_required
@staff_required
def add_stock_view(request):
    stock_list = Stock.objects.all()
    form = forms.AddStockForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Stock is added successfully')
        return redirect('myadmin:add_stock')


    context = {'form':form, 'stock_list':stock_list}
    return render(request, 'myadmin/add_stock.html', context)


@login_required
@staff_required
def delete_stock_view(request, pk):
    stock = Stock.objects.get(pk=pk)
    stock.delete()
    messages.success(request, 'Stock is deleted successfully')
    return redirect('myadmin:add_stock')


def edit_use_buy_stock_view(request, pk):
    user_stock = BuyStock.objects.get(pk=pk)
    form = forms.EditUserBuyStockForm(request.POST or None, instance=user_stock)
    if form.is_valid():
        form.save()
        messages.success(request, 'Purchased Stock is updated successfully')
        return redirect('myadmin:detail_user', pk=user_stock.user.pk)

    context = {'form':form}
    return render(request, 'myadmin/edit_user_buystock.html', context)