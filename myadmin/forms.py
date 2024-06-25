from django import forms
from django.contrib.auth.forms import UserCreationForm

from account.models import CustomUser, Profile
from stock.models import Stock


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ['date_created', 'user']

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })


class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })


class AddStockForm(forms.ModelForm):
    class Meta:
        model = Stock
        # fields = '__all__'
        fields = ['company', 'price_per_bond', 'picture']
        labels = {
            'company': 'Company Name',
            'price_per_bond': 'Price Per Bond',
            'picture': 'Company Logo Image - (optional)',
        }

    def __init__(self, *args, **kwargs):
        super(AddStockForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
            })
