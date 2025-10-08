from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from apps.root_users.models import RootUser


class AdminRequest(models.Model):
    """
    Admins submit requests without specifying a RootUser.
    Requests remain PENDING until a RootUser reviews them.
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    national_id = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField(max_length=120, unique=True)

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_requests"
        ordering = ["-requested_at"]

    def __str__(self):
        return f"AdminRequest {self.id} - {self.status}"


class AdminUser(models.Model):
    """
    Admin users created and managed by RootUsers.
    Each admin has authentication credentials and profile info.
    """
    root = models.ForeignKey(RootUser, on_delete=models.CASCADE, related_name="admins")

    username = models.CharField(max_length=80, unique=True)
    password_hash = models.CharField(max_length=255)

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    national_id = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField(max_length=120, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_users"
        ordering = ["-created_at"]

    def set_password(self, raw_password):
        """Hashes and sets the admin's password."""
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """Validates a password against the stored hash."""
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.username} ({self.root.username})"


class RootUserToken(models.Model):
    """
    Simple token model to authenticate RootUser actions.
    (You can still keep it for manual tokens or fallback auth.)
    """
    key = models.CharField(max_length=64, unique=True)
    root_user = models.ForeignKey(RootUser, on_delete=models.CASCADE, related_name="tokens")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "root_user_tokens"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Token {self.key} for {self.root_user.username}"
