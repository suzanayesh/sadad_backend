from django.db import models

from apps.debts.models import Debt


class Calculation(models.Model):
    debt = models.OneToOneField(Debt, on_delete=models.CASCADE, related_name="calculation")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "calculations"

    def __str__(self):
        return f"Calculation for Debt {self.debt.id}"
