from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.name  

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=14, decimal_places=2)  
    occurred_on = models.DateField()
    note = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f'{self.occurred_on} - {self.category} - {self.amount}'
