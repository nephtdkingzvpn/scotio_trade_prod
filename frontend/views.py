from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('account:customer_dashboard')
    return render(request, 'frontend/index.html')
