from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils import timezone

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

# -------------------------------
# New Inventory Record Model for Charts/Reports
# -------------------------------
class InventoryRecord(models.Model):
    vendor = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    purchase_rate = models.FloatField()
    sales_rate = models.FloatField()
    sold_quantity = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)  

    def remaining_quantity(self):
        return self.quantity - self.sold_quantity

    def __str__(self):
        return f"{self.product} from {self.vendor} ({self.date_created.strftime('%Y-%m-%d')})"