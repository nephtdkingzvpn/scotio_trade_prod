import random
from django.contrib import messages
from django.shortcuts import render, redirect
from decimal import Decimal

from .models import BuyStock, BuySoldStock
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

        BuySoldStock.objects.create(user=request.user, stock=bought.stock, sold_for=bought.amount, transaction_type='Bought')

        messages.success(request, 'Your Stock purchase was successful')
        return redirect('stock:stock_list')
    return render(request, 'stock/buy_stock.html', {'form':form})


def sell_stock_view(request):
    if request.method == 'POST':
        stock_id = request.POST['stock_id']
        s_amount = Decimal(request.POST['s_amount'])
        stock = BuyStock.objects.get(id=stock_id)
        user_profile = Profile.objects.get(user=request.user)

        if s_amount > stock.get_live_profit():
            messages.error(request, 'The amount entered is higher than the available balance for this stock')
            return redirect('stock:stock_list')
        
        sell_balance = stock.get_live_profit() - s_amount
        
        stock.amount = (sell_balance/Decimal(stock.percent_live)) 
        stock.sold_for = s_amount
        stock.save()

        user_profile.dollar_balance += s_amount
        user_profile.save()

        BuySoldStock.objects.create(user=request.user, stock=stock.stock, sold_for=s_amount, transaction_type='Sold')

        if sell_balance <= 0:
            stock.is_active = False
            stock.save()

        messages.success(request, 'Stock Sold successfully')
        return redirect('stock:stock_list')
    return redirect('stock:stock_list')


def stock_trade_history_view(request):
    sold_stocks = BuySoldStock.objects.filter(user=request.user)

    context = {'sold_stocks':sold_stocks}
    return render(request, 'stock/stock_transaction.html', context)