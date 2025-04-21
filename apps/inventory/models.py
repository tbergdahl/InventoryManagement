from django.db import models

class InventoryItem(models.Model):   # Normal Django model
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    min_quantity = models.IntegerField(null=True, blank=True)
    max_quantity = models.IntegerField(null=True, blank=True)
    template_message = models.TextField(null=True, blank=True)

    @property
    def is_perishable(self):
        return self.expiry_date is not None

    def __str__(self):
        return self.name

class ThresholdSetting(models.Model):
    product = models.CharField(max_length=100)
    min_quantity = models.PositiveIntegerField()
    max_quantity = models.PositiveIntegerField()
    color = models.CharField(max_length=20, default="#000000")
    template_message = models.CharField(max_length=255, default="Only {stock} units left")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Threshold for {self.product}"

class InventoryRecord(models.Model):  
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    recorded_at = models.DateTimeField()

    def __str__(self):
        return f"{self.product} - {self.quantity} at {self.recorded_at.strftime('%Y-%m-%d')}"
