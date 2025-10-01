from django.db import models

class Creditor(models.Model):
    full_name = models.CharField(max_length=150)
    national_id = models.CharField(max_length=32, unique=True)
    phone = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = "creditors"

    def __str__(self):
        return self.full_name
