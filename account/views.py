from decimal import Decimal, ROUND_DOWN
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
import datetime

# my imports
from .get_aapl_data import get_data, get_live_crypto_rates, convert_crypto_to_usd
from .models import BankAccount, Profile, BankTransaction, Balance
from . import forms

def login_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('frontend:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('account:login')
            
    return render(request, 'frontend/login.html')


def customer_dashboard(request):
    rates = get_live_crypto_rates()
    balance = Balance.objects.get(user=request.user)

    conversions = None

    if rates:
        # Convert to Bitcoin
        bitcoin_rate = convert_crypto_to_usd(balance.bitcoin, rates, crypto_type='bitcoin')

        ethereum_rate = convert_crypto_to_usd(balance.etheriun, rates, crypto_type='ethereum')

    context = {'rates':rates, 'btc':bitcoin_rate, 'eth':ethereum_rate}

    return render(request, 'account/customer/customer_dashboard.html', context)


def combined_data_view(request):
    # Fetch data for AAPL and MSFT
    data_aapl = get_data('AAPL')
    data_msft = get_data('MSFT')
    
    if data_aapl is None or data_msft is None:
        return JsonResponse({'error': 'Failed to fetch data'})

    try:
        # Process AAPL data
        timestamps_aapl = data_aapl['chart']['result'][0]['timestamp']
        prices_aapl = data_aapl['chart']['result'][0]['indicators']['quote'][0]['close']
        dates_aapl = [datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps_aapl]

        # Process MSFT data
        timestamps_msft = data_msft['chart']['result'][0]['timestamp']
        prices_msft = data_msft['chart']['result'][0]['indicators']['quote'][0]['close']
        dates_msft = [datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps_msft]

        # Ensure dates match
        if dates_aapl != dates_msft:
            return JsonResponse({'error': 'Date mismatch between datasets'})

        # Prepare data for Chart.js
        chart_data = {
            'labels': dates_aapl,
            'datasets': [
                {
                    'label': 'AAPL',
                    'data': prices_aapl,
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1,
                    'fill': False
                },
                {
                    'label': 'MSFT',
                    'data': prices_msft,
                    'borderColor': 'rgba(153, 102, 255, 1)',
                    'borderWidth': 1,
                    'fill': False
                }
            ]
        }
        
        return JsonResponse(chart_data)
    except (KeyError, IndexError) as e:
        print("Error processing data:", e)
        return JsonResponse({'error': 'Failed to process data'})


def exchange_view(request):
    return render(request, 'account/customer/exchange.html', )


def crypto_wallet_view(request):
    rates = get_live_crypto_rates()
    balance = Balance.objects.get(user=request.user)

    conversions = None

    if rates:
        # Convert to Bitcoin
        bitcoin_rate = convert_crypto_to_usd(balance.bitcoin, rates, crypto_type='bitcoin')

        ethereum_rate = convert_crypto_to_usd(balance.etheriun, rates, crypto_type='ethereum')
        
        usdt_rate = convert_crypto_to_usd(balance.usdt, rates, crypto_type='usdt')

    context = {'rates':rates, 'btc':bitcoin_rate, 'eth':ethereum_rate, 'usdt':usdt_rate}
    return render(request, 'account/customer/crypto_wallet.html', context)

def list_bank_accounts_view(request):
    bank_accounts = BankAccount.objects.filter(user=request.user)
    transactions = BankTransaction.objects.filter(user=request.user)

    context = {'bank_accounts':bank_accounts, 'transactions':transactions}
    return render(request, 'account/customer/list_bank_accounts.html', context)


def add_new_account_view(request):
    form = forms.AddAccountForm(request.POST or None)
    if form.is_valid():
        bank_account = form.save(commit=False)
        bank_account.user = request.user
        bank_account.save()
        messages.success(request, 'New Account added successfully')
        return redirect('account:list_bank_account')

    context = {'form':form}
    return render(request, 'account/customer/add_new_account.html', context)

def withdraw_dollars_view(request, pk):
    account_info = BankAccount.objects.get(pk=pk)
    user_profile = Profile.objects.get(user=request.user)
    form = forms.BankAccountForm(request.POST or None, instance=account_info)

    if form .is_valid():
        amount = form.cleaned_data.get('amount')
        if not account_info.is_main:
            messages.error(request, 'Sorry: A newly added account requires a verification process that could take up to 60 or more days before it can be allowed to be used for withdrawers. Thank you.')
            return redirect('account:withdraw_dollars', pk)
        if amount > user_profile.dollar_balance:
            balance = intcomma(user_profile.dollar_balance)
            my_message = f'Insufficient Balance. your dollar balance is ${balance}'
            messages.error(request, my_message)
            return redirect('account:withdraw_dollars', pk)
        
        withdrawer = form.save(commit=False)
        
        # debit the user balance
        user_profile.dollar_balance -= withdrawer.amount
        user_profile.save()

        # create a transaction object
        BankTransaction.objects.create(user=request.user, bank=withdrawer.bank,
                            holder_name=withdrawer.holder_name, account_number=withdrawer.account_number,
                            amount=withdrawer.amount, swift_iban=withdrawer.swift_iban)


        wid_message = f"Withdrawer of ${intcomma(amount)} is successful"
        messages.success(request, wid_message)
        return redirect('account:list_bank_account')

    context = {'form':form}
    return render(request, 'account/customer/withdraw_dollar.html', context)