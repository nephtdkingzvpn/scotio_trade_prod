from django.shortcuts import render

from .models import ExchangeTrade

def crypto_history_view(request):
    deposits = ExchangeTrade.objects.filter(user=request.user, exchange_type='Deposit')
    exchanges = ExchangeTrade.objects.filter(user=request.user, exchange_type='Sold')
    withdraws = ExchangeTrade.objects.filter(user=request.user, exchange_type='Withdraw')

    context = {'deposits':deposits, 'exchanges':exchanges, 'withdraws':withdraws}
    return render(request, 'account/customer/crypto_history.html', context)
