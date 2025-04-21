from django import forms
from apps.inventory.models import ThresholdSetting, InventoryItem

# Choices for item type
ITEM_TYPE_CHOICES = (
    ('perishable', 'Perishable'),
    ('non-perishable', 'Non-Perishable'),
)

# Choices for category
CATEGORY_CHOICES = (
    ('bakery', 'Bakery'),
    ('beverages', 'Beverages'),
    ('canned', 'Canned Goods'),
    ('dairy', 'Dairy'),
    ('fresh', 'Fresh Produce'),
    ('frozen', 'Frozen Foods'),
    ('other', 'Other'),
    ('snacks', 'Snacks'),
    ('supplies', 'Supplies'),
)

# Form for Inventory Item
class InventoryItemForm(forms.ModelForm):
    item_type = forms.ChoiceField(
        choices=ITEM_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Item Type"
    )

    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'count', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        item_type = self.cleaned_data.get('item_type')
        expiry_date = self.cleaned_data.get('expiry_date')

        if item_type == 'perishable' and not expiry_date:
            self.add_error('expiry_date', 'Expiry date is required for perishable items.')
        return cleaned_data

# Form for Threshold Settings
class ThresholdForm(forms.ModelForm):
    class Meta:
        model = ThresholdSetting
        fields = ['product', 'min_quantity', 'max_quantity', 'color', 'template_message']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'template_message': forms.TextInput(attrs={'placeholder': 'e.g., Only {stock} units left'}),
        }
