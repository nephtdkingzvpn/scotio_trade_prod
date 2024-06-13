from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import datetime

# my imports
from .get_aapl_data import get_aapl_data

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


def aapl_data_view(request):
    data = get_aapl_data()
    
    if data is None:
        return JsonResponse({'error': 'Failed to fetch AAPL data'})
    
    try:
        timestamps = data['chart']['result'][0]['timestamp']
        prices = data['chart']['result'][0]['indicators']['quote'][0]['close']
        
        # Convert timestamps to datetime objects
        dates = [datetime.datetime.fromtimestamp(ts) for ts in timestamps]
        
        # Prepare data for Chart.js
        chart_data = {
            'labels': [date.strftime('%Y-%m-%d') for date in dates],
            'prices': prices,
        }
        
        return JsonResponse(chart_data)
    except (KeyError, IndexError) as e:
        print("Error processing AAPL data:", e)
        return JsonResponse({'error': 'Failed to process AAPL data'})

