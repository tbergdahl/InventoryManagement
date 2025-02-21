from django.db import models
from polymorphic.models import PolymorphicModel
# Create your models here.
class InventoryItem(PolymorphicModel):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    
class PerishableInventoryItem(InventoryItem):
    expiry_date = models.DateField()
    

class NonPerishableInventoryItem(InventoryItem):
    # uhh
    pass