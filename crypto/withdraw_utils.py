from decimal import Decimal
from .models import Balance
from django.http import JsonResponse

def withdraw_crypto(user, crypto_type, crypto_amount):
    try:
        user_balance = Balance.objects.get(user=user)

        if crypto_type == 'bitcoin':
            if float(crypto_amount) > user_balance.bitcoin:
                return JsonResponse({'insuff': 'insufficientbalance'})
            user_balance.bitcoin -= float(crypto_amount)

        elif crypto_type == 'ethereum':
            if float(crypto_amount) > user_balance.ethereum:
                return JsonResponse({'insuff': 'insufficientbalance'})
            user_balance.ethereum -= float(crypto_amount)

        elif crypto_type == 'tetherusdt':
            if Decimal(crypto_amount) > user_balance.tetherusdt:
                return JsonResponse({'insuff': 'insufficientbalance'})
            user_balance.tetherusdt -= Decimal(crypto_amount)

        user_balance.save()
        return None  # Indicating successful withdrawal
    except Balance.DoesNotExist:
        return JsonResponse({'error': 'Balance not found'}, status=404)
