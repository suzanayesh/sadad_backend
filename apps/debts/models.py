from django.db import models
from django.utils import timezone
from apps.creditors.models import Creditor
from apps.admin_info.models import AdminInfo

class Debt(models.Model):
    creditor = models.ForeignKey(Creditor, on_delete=models.CASCADE, related_name="debts")
    admin = models.ForeignKey(AdminInfo, on_delete=models.CASCADE, related_name="debts")
    start_date = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)

    STATUS_CHOICES = [
        ('INCOMPLETE', 'غير مكتمل'),
        ('COMPLETE', 'مكتمل'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INCOMPLETE')

    class Meta:
        db_table = "debts"

    def __str__(self):
        return f"{self.creditor.full_name} - {self.amount} ({self.status})"
