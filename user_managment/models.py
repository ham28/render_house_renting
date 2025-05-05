from django.contrib.auth.models import AbstractUser
from django.db import models

from property_managment.models import Owner, Tenant

'''
' Custom User Model
'''

class CustomUser(AbstractUser):
    groups = models.ManyToManyField( 'auth.Group', related_name='custom_user_set', blank=True, verbose_name='groups',  help_text='The groups this user belongs to.' )
    user_permissions = models.ManyToManyField( 'auth.Permission', related_name='custom_user_set', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.' )
    user_type =  models.CharField(max_length=100, blank=True)
    function = models.CharField(max_length=100, blank=True)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)

    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True)
    # Foreign key
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE, unique=True, blank=True, null=True, related_name="user")
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, unique=True, blank=True, null=True, related_name="user")

    # Add any additional fields you want here
    @property
    def devices(self):
        return self.userdevice_set.all()

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.groups.filter(name='Admin').exists()


# The devices property is unnecessary since we have related_name='devices'
# in the UserDevice model
class UserDevice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    verification_token = models.CharField(max_length=255, null=True, blank=True)
    verification_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s device: {self.device_name}"