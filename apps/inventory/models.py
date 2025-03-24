from django.db import models
from polymorphic.models import PolymorphicModel
# Create your models here.
class InventoryItem(PolymorphicModel):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    count = models.IntegerField(default=0)

    @property
    def is_perishable(self):
        # return true if item has expiry field
        return hasattr(self, 'expiry_date')
    
class PerishableInventoryItem(InventoryItem):
    expiry_date = models.DateField()
    

class NonPerishableInventoryItem(InventoryItem):
    # uhh
    pass