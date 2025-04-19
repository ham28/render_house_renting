from django.contrib import admin

from property_managment.models import Property, Owner, LeaseContract, Tenant, PropertyImages, File, Payment

# Register your models here.

admin.site.register(Property)
admin.site.register(Owner)
admin.site.register(Tenant)
admin.site.register(PropertyImages)
admin.site.register(File)
admin.site.register(Payment)
admin.site.register(LeaseContract)