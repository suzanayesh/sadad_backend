from django.db import models

from apps.root_users.models import RootUser


class AdminRequest(models.Model):
	# Admins submit requests without knowing which RootUser will review them.
	# Remove root_user FK: requests are global and stay PENDING until a root acts.
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	national_id = models.CharField(max_length=32)
	phone = models.CharField(max_length=32)
	email = models.EmailField(max_length=120)

	STATUS_CHOICES = [
		("PENDING", "Pending"),
		("APPROVED", "Approved"),
		("REJECTED", "Rejected"),
	]
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

	requested_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "admin_requests"

	def __str__(self):
		return f"AdminRequest {self.id} ({self.status})"


class AdminUser(models.Model):
	username = models.CharField(max_length=80, unique=True)
	password_hash = models.CharField(max_length=255)
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	national_id = models.CharField(max_length=32)
	phone = models.CharField(max_length=32)
	email = models.EmailField(max_length=120)
	root_user = models.ForeignKey(RootUser, on_delete=models.CASCADE, related_name="admins")

	class Meta:
		db_table = "admin_users"

	def __str__(self):
		return f"{self.username} ({self.root_user.username})"


class RootUserToken(models.Model):
	"""Simple token model to authenticate RootUser actions.

	Fields:
	- key: randomly generated token string (32+ chars)
	- root_user: FK to RootUser
	- created_at: timestamp
	"""
	key = models.CharField(max_length=64, unique=True)
	root_user = models.ForeignKey(RootUser, on_delete=models.CASCADE, related_name="tokens")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = "root_user_tokens"

	def __str__(self):
		return f"Token {self.key} for {self.root_user.username}"
