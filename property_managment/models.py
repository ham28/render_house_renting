from django.db import models

import re
from user_managment.models import CustomUser

# Create your models here.

"""
Table des Propriétaires
"""


class Owner(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    f_name = models.CharField(max_length=255, blank=True, null=True)
    l_name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)

    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    commune = models.CharField(max_length=255, blank=True, null=True)
    quartier = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    # Foreign key
    user = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING, related_name='owner', null=True, blank=True)

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None, ):
        if not self.name:
            self.name = f"{self.f_name} {self.l_name}"

        # Call the parent class's save method to actually save the object
        super().save(*args, force_insert=False, force_update=False, using=None, update_fields=None)


    def __str__(self):
        return self.name or self.f_name or self.l_name

"""
Table des Propriétés (ou Biens Immobiliers)
"""
class Property(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    announcement_type = models.CharField(max_length=255, blank=True, null=True)
    property_type = models.CharField(max_length=255, blank=True, null=True)
    surface = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    room_nbr = models.IntegerField(blank=True, null=True)
    bath_room_nbr = models.IntegerField(blank=True, null=True)
    construction_year = models.DateField(blank=True, null=True)
    selling_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    renting_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=True)
    renting_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    property_condition = models.CharField(max_length=255, blank=True, null=True)

    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    commune = models.CharField(max_length=255, blank=True, null=True)
    quartier = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    label = models.CharField(max_length=255, blank=True, null=True)
    # Foreign key
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True,related_name="properties")

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None, ):
        label = re.findall(r'#\w+', str(self.description))
        self.label = str(label)
        if not self.name:
            self.name = f"{self.type} {self.owner.name}"

        # Call the parent class's save method to actually save the object
        super().save(*args, force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return self.name or self.property_type


"""
Table des Locataires
"""


class Tenant(models.Model):
    f_name = models.CharField(max_length=255, blank=True, null=True)
    l_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    payment_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    guarantor = models.CharField(max_length=255, blank=True, null=True)

    current_address = models.CharField(max_length=255, blank=True, null=True)


class PropertyImages(models.Model):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='assets/images/')
    # Foreign key
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')


class File(models.Model):
    description = models.TextField(blank=True, null=True)
    file = models.FileField()
    # Foreign key
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE, related_name='files')
    owner = models.ForeignKey(Owner, null=True, blank=True, on_delete=models.CASCADE, related_name='files')


"""
Table des Paiements
"""


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_type = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    # Foreign key
    tenant = models.OneToOneField(Tenant, on_delete=models.DO_NOTHING)
    property = models.OneToOneField(Property, on_delete=models.DO_NOTHING)


"""
Table des Contrats de Location
"""


class LeaseContract(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contract_status = models.BooleanField(default=True)
    rules = models.TextField()
    # Foreign key
    tenant = models.OneToOneField(Tenant, on_delete=models.DO_NOTHING)
    property = models.OneToOneField(Property, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
