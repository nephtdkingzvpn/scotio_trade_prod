from django import forms

from.models import BankAccount

class BankAccountForm(forms.ModelForm):

    class Meta:
        model = BankAccount
        fields = ['bank', 'holder_name', 'account_number', 'swift_iban', 'amount']
        labels = {
            'bank': 'Bank Name',
            'holder_name': 'Account Name',
            'account_number': 'Account Number',
            'swift_iban': 'Swift/Iban',
            'amount': 'Enter Amount',
        }


    def __init__(self, *args, **kwargs):
        super(BankAccountForm, self).__init__(*args, **kwargs)

        self.fields['bank'].widget.attrs['readonly'] = True
        self.fields['holder_name'].widget.attrs['readonly'] = True
        self.fields['account_number'].widget.attrs['readonly'] = True
        self.fields['swift_iban'].widget.attrs['readonly'] = True
        self.fields['amount'].required = True

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if not amount:
            raise forms.ValidationError('This field is required.')
        return amount
    

class AddAccountForm(forms.ModelForm):

    class Meta:
        model = BankAccount
        fields = ['bank', 'holder_name', 'account_number', 'swift_iban']
        labels = {
            'bank': 'Bank Name',
            'holder_name': 'Account Name',
            'account_number': 'Account Number',
            'swift_iban': 'Swift/Iban - optional',
        }

    def __init__(self, *args, **kwargs):
        super(AddAccountForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })