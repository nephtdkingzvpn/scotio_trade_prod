from django import forms

from.models import BuyStock, Stock

class BuyStockForm(forms.ModelForm):
    class Meta:
        model = BuyStock
        fields = ['stock', 'amount']
        labels = {
            'stock': 'Select Stock to Buy',
            'amount': 'Enter Amount'
        }

    def __init__(self, *args, **kwargs):
        super(BuyStockForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })

        # default_stock = Stock.objects.get(company='Tesla')
        # self.initial['stock'] = default_stock