import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from property_managment.DjangoObjectType import TenantType, PropertyType, OwnerType, PropertyImageType, \
    PaymentType, LeaseContractType
from property_managment.models import Tenant, Property, LeaseContract, Payment, Owner


# Assuming these types are already defined elsewhere in your code
# from .types import TenantType, PropertyType, OwnerType, AddressType, PropertyImageType, PaymentType, LeaseContractType

class PropertyImage:
    pass


class Query(graphene.ObjectType):
    """GraphQL Query class for all object types"""

    # Tenant queries
    tenants = graphene.List( TenantType, search=graphene.String(), description="List all tenants, optionally filtered by search term" )
    tenant = graphene.Field( TenantType, id=graphene.Int(required=True), description="Get a specific tenant by ID" )

    # Property queries
    properties = graphene.List( PropertyType, status=graphene.Boolean(), type=graphene.String(), search=graphene.String(), description="List all properties, optionally filtered by status, type, or search term" )
    property = graphene.Field( PropertyType, id=graphene.Int(required=True), description="Get a specific property by ID" )

    # Owner queries
    owners = graphene.List( OwnerType, type=graphene.String(), search=graphene.String(), description="List all owners, optionally filtered by type or search term" )
    owner = graphene.Field( OwnerType, id=graphene.Int(required=True), description="Get a specific owner by ID" )

    # Property Image queries
    property_images = graphene.List( PropertyImageType, property_id=graphene.Int(), description="List all property images, optionally filtered by property ID" )
    property_image = graphene.Field( PropertyImageType, id=graphene.Int(required=True), description="Get a specific property image by ID" )

    # Payment queries
    payments = graphene.List( PaymentType, tenant_id=graphene.Int(), property_id=graphene.Int(), status=graphene.String(), start_date=graphene.Date(), end_date=graphene.Date(), description="List all payments, optionally filtered by tenant, property, status, or date range" )
    payment = graphene.Field( PaymentType, id=graphene.Int(required=True), description="Get a specific payment by ID" )

    # Lease Contract queries
    lease_contracts = graphene.List( LeaseContractType, tenant_id=graphene.Int(), property_id=graphene.Int(), active=graphene.Boolean(), description="List all lease contracts, optionally filtered by tenant, property, or active status" )
    lease_contract = graphene.Field( LeaseContractType, id=graphene.Int(required=True), description="Get a specific lease contract by ID" )

    # Tenant resolver methods
    def resolve_tenants(self, info, search=None):
        queryset = Tenant.objects.all()

        if search:
            filter = (
                    Q(f_name__icontains=search) |
                    Q(l_name__icontains=search) |
                    Q(email__icontains=search) |
                    Q(phone__icontains=search)
            )
            queryset = queryset.filter(filter)

        return queryset

    def resolve_tenant(self, info, id):
        try:
            return Tenant.objects.get(id=id)
        except Tenant.DoesNotExist:
            return None

    # Property resolver methods
    def resolve_properties(self, info, status=None, type=None, search=None):
        queryset = Property.objects.all()

        if status is not None:
            queryset = queryset.filter(status=status)

        if type:
            queryset = queryset.filter(type=type)

        if search:
            filter = (
                    Q(name__icontains=search) |
                    Q(description__icontains=search) |
                    Q(address__address__icontains=search) |
                    Q(address__region__icontains=search) |
                    Q(address__district__icontains=search) |
                    Q(address__commune__icontains=search) |
                    Q(address__quartier__icontains=search)
            )
            queryset = queryset.filter(filter)

        return queryset

    def resolve_property(self, info, id):
        try:
            return Property.objects.get(id=id)
        except Property.DoesNotExist:
            return None

    # Owner resolver methods
    def resolve_owners(self, info, type=None, search=None):
        queryset = Owner.objects.all()

        if type:
            queryset = queryset.filter(type=type)

        if search:
            filter = (
                    Q(f_name__icontains=search) |
                    Q(l_name__icontains=search) |
                    Q(email__icontains=search) |
                    Q(phone__icontains=search)
            )
            queryset = queryset.filter(filter)

        return queryset

    def resolve_owner(self, info, id):
        try:
            return Owner.objects.get(id=id)
        except Owner.DoesNotExist:
            return None


    # Property Image resolver methods
    def resolve_property_images(self, info, property_id=None):
        queryset = PropertyImage.objects.all()

        if property_id:
            queryset = queryset.filter(property_id=property_id)

        return queryset

    def resolve_property_image(self, info, id):
        try:
            return PropertyImage.objects.get(id=id)
        except PropertyImage.DoesNotExist:
            return None

    # Payment resolver methods
    def resolve_payments(self, info, tenant_id=None, property_id=None, status=None, start_date=None, end_date=None):
        queryset = Payment.objects.all()

        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)

        if property_id:
            queryset = queryset.filter(property_id=property_id)

        if status:
            queryset = queryset.filter(status=status)

        if start_date:
            queryset = queryset.filter(payment_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(payment_date__lte=end_date)

        return queryset

    def resolve_payment(self, info, id):
        try:
            return Payment.objects.get(id=id)
        except Payment.DoesNotExist:
            return None

    # Lease Contract resolver methods
    def resolve_lease_contracts(self, info, tenant_id=None, property_id=None, active=None):
        queryset = LeaseContract.objects.all()

        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)

        if property_id:
            queryset = queryset.filter(property_id=property_id)

        if active is not None:
            queryset = queryset.filter(contract_status=active)

        return queryset

    def resolve_lease_contract(self, info, id):
        try:
            return LeaseContract.objects.get(id=id)
        except LeaseContract.DoesNotExist:
            return None