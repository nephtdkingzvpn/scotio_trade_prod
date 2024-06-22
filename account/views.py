from decimal import Decimal, ROUND_DOWN
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import JsonResponse
import datetime
import requests

# my imports
from .get_aapl_data import (get_data, convert_crypto_to_usd, convert_usd_to_crypto)
from .fetch_crypto import fetch_crypto_with_caching
from .fetch_chistory import fetch_history_with_caching
from .models import BankAccount, Profile, BankTransaction, Balance
from . import forms
from .email_utils import send_html_email


def login_user_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account:customer_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('account:login')
            
    return render(request, 'frontend/login.html')


def logout_user_view(request):
    logout(request)
    return redirect('account:login')


def customer_dashboard(request):
    try:
        rates = fetch_crypto_with_caching()
        balance = Balance.objects.get(user=request.user)

        conversions = None

        if rates:
            # Convert to Bitcoin
            bitcoin_rate = convert_crypto_to_usd(balance.bitcoin, rates, crypto_type='bitcoin')

            ethereum_rate = convert_crypto_to_usd(balance.etheriun, rates, crypto_type='ethereum')

            context = {'rates':rates, 'btc':bitcoin_rate, 'eth':ethereum_rate, 'balance':balance}
        else:
            context = {}
    except:
        context = {'rates':'fetching', 'btc':'fetching', 'eth':'fetching', 'balance':balance}
    finally:
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
    if request.method == "POST":
        user = Profile.objects.get(user=request.user)
        balance = Balance.objects.get(user=request.user)
        selected_option = request.POST.get('selected_option')
        amount = request.POST.get('amount')

        # check if amount in input is less than the user"s balance
        if Decimal(amount) > user.dollar_balance:
            my_message = f'Insufficient balance, your dollar balance is ${intcomma(user.dollar_balance)}'
            messages.error(request, my_message)
            return redirect('account:exchange_view')
        
        if Decimal(amount) < Decimal(100):
            messages.error(request, 'Exchange of below $100 is not allowed.')
            return redirect('account:exchange_view')

        if selected_option:
            rates = fetch_crypto_with_caching()
            if rates is not None:
                converted = convert_usd_to_crypto(amount, rates, crypto_type=selected_option)
                c_crypto = converted[selected_option]
                if converted:
                    if selected_option == 'bitcoin':
                        balance.bitcoin = round(balance.bitcoin + float(c_crypto), 9)
                    elif selected_option == 'ethereum':
                        balance.etheriun = round(balance.etheriun + float(c_crypto), 9)
                    elif selected_option == 'usdt':
                        balance.usdt += c_crypto

                    balance.save()
                    user.dollar_balance -= Decimal(amount)
                    user.save()
                    my_message = f"A ${intcomma(amount)} worth of ({selected_option} coin) have been added to your {selected_option} wallet. Please click the crypto wallet link to view your transaction history"
                    messages.success(request, my_message)
                    return redirect('account:exchange_view')
                else:
                    messages.erroe(request, 'Something went wrong, please try again')
                    return redirect('account:exchange_view')

    return render(request, 'account/customer/exchange.html', )


def exchange_crypto_tousd_view(request):
    if request.method == "POST":
        user = Profile.objects.get(user=request.user)
        balance = Balance.objects.get(user=request.user)
        selected_option = request.POST.get('selected_option')
        amount = request.POST.get('amount')
        

        if Decimal(amount) < Decimal(100):
            messages.error(request, 'Exchange of below $100 is not allowed.')
            return redirect('account:exchange_view')

        if selected_option:
            rates = fetch_crypto_with_caching()

            if rates is not None:
                usd_to_crypto = convert_usd_to_crypto(amount, rates, crypto_type=selected_option)
                c_crypto = usd_to_crypto[selected_option]

                if usd_to_crypto:
                    m_message = f"Insufficient {selected_option} balance, please check your {selected_option} balance and try again."

                    if selected_option == 'bitcoin':
                        if c_crypto > balance.bitcoin:
                            messages.error(request, m_message)
                            return redirect('account:exchange_view')
                        balance.bitcoin = round(balance.bitcoin - float(c_crypto), 9)
                    elif selected_option == 'ethereum':
                        if c_crypto > balance.etheriun:
                            messages.error(request, m_message)
                            return redirect('account:exchange_view')
                        balance.etheriun = round(balance.etheriun - float(c_crypto), 9)
                    elif selected_option == 'usdt':
                        if c_crypto > balance.usdt:
                            messages.error(request, m_message)
                            return redirect('account:exchange_view')
                        balance.usdt -= c_crypto

                    balance.save()
                    user.dollar_balance += Decimal(amount)
                    user.save()

                    my_message = f"Your {selected_option} to dollar exchange was successful, ${intcomma(Decimal(amount))} have been added to your dollar balance."
                    messages.success(request, my_message)
                    return redirect('account:exchange_view')
                else:
                    messages.error(request, 'Something went wrong, please try again')
                    return redirect('account:exchange_view')
            
            
    return render(request, 'account/customer/exchange.html', )

def crypto_wallet_view(request):
    rates = fetch_crypto_with_caching()
    balance = Balance.objects.get(user=request.user)

    conversions = None

    if rates:
        # Convert to Bitcoin
        bitcoin_rate = convert_crypto_to_usd(balance.bitcoin, rates, crypto_type='bitcoin')

        ethereum_rate = convert_crypto_to_usd(balance.etheriun, rates, crypto_type='ethereum')
        
        usdt_rate = convert_crypto_to_usd(balance.usdt, rates, crypto_type='usdt')

        context = {'rates':rates, 'btc':bitcoin_rate, 'eth':ethereum_rate, 'usdt':usdt_rate}
    else:
        context = {}
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


def delete_account_view(request, pk):
    bank_account = BankAccount.objects.get(pk=pk)
    bank_account.delete()
    messages.success(request, 'Bank account was deleted successfully')
    return redirect('account:list_bank_account')

def withdraw_dollars_view(request, pk):
    account_info = BankAccount.objects.get(pk=pk)
    user_profile = Profile.objects.get(user=request.user)
    form = forms.BankAccountForm(request.POST or None, instance=account_info)

    if form .is_valid():
        amount = form.cleaned_data.get('amount')
        if not account_info.is_main:
            messages.error(request, 'Sorry: For your security, This newly added account requires a verification process that could take up to 60 days before it will be available for withdrawer. Contact our help center for more information.')
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


def crypto_price_history(request):
    data = fetch_history_with_caching()

    if data is not None:
        prices = data['prices']
        timestamps = [price[0] for price in prices]
        prices = [price[1] for price in prices]
        return JsonResponse({'timestamps': timestamps, 'prices': prices})
    else:
        pass


def analytics_view(request):
    return render(request, 'account/customer/analytics.html')


def help_center_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        template_name = 'emails/email_from_customer.html'
        print(name,email,message,subject)
        try:
            send_html_email('Customer Message', template_name, context)
            messages.success(request, 'Your message is sent successfully, a customer care representative will get back to you as soon as possible.')
        except:
            messages.error(request, 'Message Failed, please try again')
        finally:
            return redirect('account:help_center')

    return render(request, 'account/customer/help_center.html')