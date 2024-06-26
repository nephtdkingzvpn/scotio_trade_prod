import random
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import BuyStock
from . import forms
from account.models import Profile

def stock_list_view(request):
    active_stocks = BuyStock.objects.filter(user=request.user,is_active=True)

    context = {'active_stocks':active_stocks}
    return render(request, 'stock/stock_list.html', context)


def buy_new_stock_view(request):

    float_numbers = [2.34,0.3, 0.5,2.52, 1.0, 1.03,2.03, 1.05, 1.25,2.0,  1.43, 1.57, 1.72, 1.86, 1.90,1.23,  2.3,2.08,0.7, 2.90]

    user_profile = Profile.objects.get(user=request.user)
    form = forms.BuyStockForm(request.POST or None)
    if form.is_valid():
        bought = form.save(commit=False)
        if bought.amount > user_profile.dollar_balance:
            messages.error(request, 'insufficient Balance, please check your balance and try again')
            return redirect('stock:buy_new_stock')
        if bought.amount <= 59:
            messages.error(request, 'Sorry, we do not accept a purchase below 60 dollars')
            return redirect('stock:buy_new_stock')

        bought.user = request.user
        bought.percent_live = float(random.choice(float_numbers))
        bought.save()
        user_profile.dollar_balance -= bought.amount
        user_profile.save()

        messages.success(request, 'Your Stock purchase was successful')
        return redirect('stock:stock_list')
    return render(request, 'stock/buy_stock.html', {'form':form})


def sell_stock_view(request):
    if request.method == 'POST':
        stock_id = request.POST['stock_id']
        stock = BuyStock.objects.get(id=stock_id)
        user_profile = Profile.objects.get(user=request.user)
        stock.is_active = False
        stock.sold_for = stock.get_live_profit()
        stock.save()
        user_profile.dollar_balance += stock.get_live_profit()
        user_profile.save()
        messages.success(request, 'Stock Sold successfully')
    return redirect('stock:stock_list')