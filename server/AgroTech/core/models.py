import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_farmer = models.BooleanField(default=False)
    is_organisation = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='users', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='users', related_query_name='user')
    def is_farmer(self):
        return self.is_farmer

    def is_organisation(self):
        return self.is_organisation


class KisanBima(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer = models.OneToOneField('Farmer', on_delete=models.CASCADE, related_name='insurance_policy')
    policy_no = models.CharField(max_length=100, null=False)
    aadhar_no = models.CharField(max_length=12, unique=True, null=False)
    pan_no = models.CharField(max_length=10, unique=True, null=False)

    def __str__(self):
        return f"Policy: {self.policy_no} for Farmer: {self.farmer_id}"


class Farmer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer')
    phone = models.CharField(max_length=10, unique=True, null=False, default='0000000000')
    state = models.CharField(max_length=100, null=False)
    district = models.CharField(max_length=100, null=False)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    no_orders_delivered = models.IntegerField(default=0)
    no_orders_pending = models.IntegerField(default=0)
    no_defaults = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Farmer"

    def check_id(self):
        """Validate Aadhar and PAN with the associated KisanBima object."""
        if not hasattr(self, 'insurance_policy') or self.insurance_policy is None:
            return False
        if self.insurance_policy.aadhar_no != self.aadhar_no or self.insurance_policy.pan_no != self.pan_no:
            return False
        return True

    def check_status(self):
        """Ensures that the land area is valid and uses parent status check."""
        return self.land_area >= 0.5


class Organisation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='organisation')
    phone = models.CharField(max_length=10, unique=True, null=False, default='0000000000')
    gstin = models.CharField(max_length=15, unique=True, null=False)
    state = models.CharField(max_length=100, null=False)
    no_orders_received = models.IntegerField(default=0)
    no_orders_pending = models.IntegerField(default=0)
    no_defaults = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Organisation"


class Contract(models.Model):
    contract_id = models.CharField(max_length=100, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    # Add fields that integrate with Farmer
