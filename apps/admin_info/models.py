from django.db import models
from django.utils import timezone
from apps.root_users.models import RootUser

class AdminInfo(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    business_name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=120, unique=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    requested_at = models.DateTimeField(default=timezone.now)
    approved_at = models.DateTimeField(null=True, blank=True)

    approved_by_root = models.ForeignKey(
        RootUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_admins"
    )

    class Meta:
        db_table = "admin_info"

    def __str__(self):
        return f"{self.business_name} ({self.status})"
