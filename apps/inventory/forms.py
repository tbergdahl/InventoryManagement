from django import forms

ITEM_TYPE_CHOICES = (
    ('perishable', 'Perishable'),
    ('non-perishable', 'Non-Perishable'),
)

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

class InventoryItemForm(forms.Form):
    item_type = forms.ChoiceField(choices=ITEM_TYPE_CHOICES, widget=forms.RadioSelect)
    name = forms.CharField(max_length=100)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    count = forms.IntegerField(min_value=0)
    expiry_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Required for perishable items."
    )

    def clean(self):
        cleaned_data = super().clean()
        item_type = cleaned_data.get('item_type')
        expiry_date = cleaned_data.get('expiry_date')

        if item_type == 'perishable' and not expiry_date:
            self.add_error('expiry_date', 'Expiry date is required for perishable items.')
        return cleaned_data