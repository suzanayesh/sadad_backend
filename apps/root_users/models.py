from django.db import models

class RootUser(models.Model):
    username = models.CharField(max_length=80, unique=True)
    password_hash = models.CharField(max_length=255)

    class Meta:
        db_table = "root_users"

    def __str__(self):
        return self.username
