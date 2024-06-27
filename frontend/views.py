from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('myadmin:admin_dashboard')
        else:
            return redirect('account:customer_dashboard')
    return render(request, 'frontend/index.html')
