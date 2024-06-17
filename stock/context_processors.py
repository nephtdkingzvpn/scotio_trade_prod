from .models import BuyStock

def universal_stock_list(request):
    # Fetch objects from the database
    if request.user.is_authenticated:
        stock_list = BuyStock.objects.filter(user=request.user, is_active=True)[:5]

        return {
            'stock_list': stock_list,
        }
    else:
        return {}

