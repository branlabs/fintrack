from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): 
        return self.name  

class Transaction(models.Model):
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='transactions')
    amount = models.DecimalField(max_digits=14, decimal_places=2, help_text="Số tiền chi).")
    occurred_on = models.DateField(db_index=True)
    note = models.CharField(max_length=255, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-occurred_on', '-id']
        indexes = [
            models.Index(fields=['category', 'occurred_on'], name='idx_tx_cat_date'),
        ]

    def __str__(self):
        return f'{self.occurred_on} - {self.category} - {self.amount}'
 