from django import forms
from .models import PerishableInventoryItem


class PerishableInventoryItemForm(forms.ModelForm):
    class Meta:
        model = PerishableInventoryItem
        fields = ['name', 'category', 'count', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }