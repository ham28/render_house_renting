import logging
import graphene

from graphql import GraphQLError

from django.db.models import Q
from django.contrib.auth import get_user_model

from .mutations import AddTenantMutation, AddPropertyMutation, AddOwnerMutation, \
    AddPropertyImagesMutation, AddPaymentMutation, AddLeaseContractMutation
from .DjangoObjectType import TenantType, PropertyType, OwnerType, PropertyImageType, \
    PaymentType, LeaseContractType
from .models import Tenant, Property, LeaseContract, Payment, Owner, PropertyImages
from .utils import get_region

# Assuming these types are already defined elsewhere in your code

logger = logging.getLogger("django")



class Query(graphene.ObjectType):
    """GraphQL Query class for all object types"""
    # Tenant queries
    tenants = graphene.List( TenantType, id=graphene.Int(required=True), search=graphene.String(), description="List all tenants, optionally filtered by search term" )
    # Property queries
    properties = graphene.List( PropertyType, id=graphene.Int(required=False), announcement_type=graphene.String(required=False), status=graphene.Boolean(), type=graphene.String(), search=graphene.String(), user_id=graphene.Int(required=False), owner_id=graphene.Int(required=False), province_=graphene.String(required=False), region_=graphene.String(required=False), description="List all properties, optionally filtered by status, type, or search term and more" )
    # Owner queries
    owners = graphene.List( OwnerType, id=graphene.Int(required=True), type=graphene.String(), search=graphene.String(), description="List all owners, optionally filtered by type or search term or by ID" )
    # Property Image queries
    property_images = graphene.List( PropertyImageType, image_id=graphene.Int(required=True), property_id=graphene.Int(), description="List all property images, optionally filtered by property ID" )

    # Payment queries
    payments = graphene.List( PaymentType, tenant_id=graphene.Int(), property_id=graphene.Int(), status=graphene.String(), start_date=graphene.Date(), end_date=graphene.Date(), description="List all payments, optionally filtered by tenant, property, status, or date range" )
    payment = graphene.Field( PaymentType, id=graphene.Int(required=True), description="Get a specific payment by ID" )

    # Lease Contract queries
    lease_contracts = graphene.List( LeaseContractType, tenant_id=graphene.Int(), property_id=graphene.Int(), active=graphene.Boolean(), description="List all lease contracts, optionally filtered by tenant, property, or active status" )
    lease_contract = graphene.Field( LeaseContractType, id=graphene.Int(required=True), description="Get a specific lease contract by ID" )

    # Tenant resolver methods
    def resolve_tenants(self, info, id=None, search=None):
        try:
            if id:
                return Tenant.objects.get(id=id)
            if search:
                queryset = Tenant.objects.all()
                filter = (
                        Q(f_name__icontains=search) |
                        Q(l_name__icontains=search) |
                        Q(email__icontains=search) |
                        Q(phone__icontains=search)
                )
                queryset = queryset.filter(filter)
                return queryset

            return Tenant.objects.all()

        except Tenant.DoesNotExist:
            raise GraphQLError(f'Tenant {id} {search} does not exist')
        except Exception as e:
            raise Exception(f'Exception {e} ')


    # Property resolver methods
    def resolve_properties(self, info,
                                 id=None,
                                 announcement_type=None,
                                 province_=None,
                                 region_=None,
                                 status=None,
                                 type=None,
                                 search=None,
                                 user_id=None,
                                 owner_id=None):
        """
        Fonction unifiée qui gère tous les cas de requêtes de propriété

        Args:
            info: Contexte GraphQL
            id: ID de la propriété à rechercher
            announcement_type: Type d'annonce
            province_: Province pour filtrer
            region_: Région pour filtrer
            status: Statut de la propriété
            type: Type de propriété
            search: Terme de recherche
            user_id: ID de l'utilisateur pour ses propriétés
            owner_id: ID du propriétaire pour ses propriétés

        Returns:
            QuerySet ou instance de Property selon les paramètres fournis
        """
        try:
            # Cas 1: Recherche par ID ou announcement_type (single property)
            if id or announcement_type:
                if id:
                    return Property.objects.get(id=id)
                else:
                    return Property.objects.get(announcement_type__iexact=announcement_type)

            # Cas 2: Recherche par propriétaire (user_id ou owner_id)
            if user_id or owner_id:
                owner = None
                if user_id:
                    User = get_user_model()
                    owner = User.objects.get(id=user_id).owner
                elif owner_id:
                    owner = Owner.objects.get(id=owner_id)

                if owner:
                    return owner.properties.all()
                return None

            # Cas 3: Recherche par province ou région
            if province_ or region_:
                if province_:
                    regions = get_region(province_)
                    query = Q()
                    for region in regions:
                        query |= Q(region__iexact=region)
                    return Property.objects.filter(query)

                if region_:
                    return Property.objects.filter(region__iexact=region_)

            # Cas 4: Recherche générale avec filtres (status, type, search)
            queryset = Property.objects.all()

            if status is not None:
                queryset = queryset.filter(status=status)

            if type:
                queryset = queryset.filter(type=type)

            if search:
                filter = (
                        Q(name__icontains=search) |
                        Q(description__icontains=search) |
                        Q(address__icontains=search) |
                        Q(region__icontains=search) |
                        Q(district__icontains=search) |
                        Q(commune__icontains=search) |
                        Q(quartier__icontains=search)
                )
                queryset = queryset.filter(filter)

            return queryset

        except Property.DoesNotExist:
            logger.info(
                f"Property DoesNotExist: ID={id}, announcement_type={announcement_type}, region={region_}, province={province_}")
            return None
        except Owner.DoesNotExist:
            logger.info(f"Owner DoesNotExist: user_id={user_id}, owner_id={owner_id}")
            return None
        except Exception as e:
            logger.error(f"Exception while resolving property: {e}")
            raise Exception(f"Erreur lors de la récupération des propriétés: {e}")


    # Owner resolver methods
    def resolve_owners(self, info, id=None, type=None, search=None):
        try:
            if id:
                return Owner.objects.get(id=id)

            if type or search:
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

        except Owner.DoesNotExist:
            return None


    # Property Image resolver methods
    def resolve_property_images(self, info, image_id=None, property_id=None):
        try:
            if image_id:
                return PropertyImages.objects.get(id=id)

            if property_id:
                queryset = PropertyImages.filter(property_id=property_id)
                return queryset

        except PropertyImages.DoesNotExist:
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


class Mutation(graphene.ObjectType):
    add_tenant = AddTenantMutation.Field()
    add_property = AddPropertyMutation.Field()
    add_owner = AddOwnerMutation.Field()
    add_property_image = AddPropertyImagesMutation.Field()
    add_payment = AddPaymentMutation.Field()
    add_leaser_contract = AddLeaseContractMutation.Field()



