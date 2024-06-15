from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import datetime

# my imports
from .get_aapl_data import get_data

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
    return render(request, 'account/customer/customer_dashboard.html')


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
    return render(request, 'account/customer/exchange.html')


def crypto_wallet_view(request):
    return render(request, 'account/customer/crypto_wallet.html')