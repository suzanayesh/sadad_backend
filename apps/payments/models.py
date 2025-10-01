from django.db import models
from django.utils import timezone
from apps.debts.models import Debt

class Payment(models.Model):
    debt = models.ForeignKey(Debt, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment {self.amount} for Debt {self.debt.id}"
