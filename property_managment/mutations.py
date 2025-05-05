import logging
import graphene
from graphql import GraphQLError
from graphene_file_upload.scalars import Upload

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from .DjangoObjectType import PropertyType, TenantType, OwnerType, PropertyImageType, \
    PaymentType, LeaseContractType
from .models import Property, Tenant, Owner, PropertyImages, Payment, LeaseContract
from user_managment.djangoObjectType import UserType

logger = logging.getLogger(__name__)

class PropertyImageInput(graphene.InputObjectType):
    """Input type for property images"""
    description = graphene.String(required=True, description="Description of the image")
    image = Upload(required=True, description="The property image file")


class AddPropertyMutation(graphene.Mutation):
    """Mutation to add a new property with images"""
    class Arguments:
        # Basic property information
        name = graphene.String(required=False, description="Name of the property")
        type = graphene.String(required=False, description="Type of managment")
        property_type = graphene.String(required=False, description="Type of property (e.g., apartment, house)")
        surface = graphene.Decimal(required=False, description="Total surface area")
        room_nbr = graphene.Int(required=False, description="Number of rooms")
        bath_room_nbr = graphene.Int(required=False, description="Number of bathrooms")
        construction_year = graphene.Date(required=False, description="Year of construction")

        # Financial details
        selling_price = graphene.Decimal(required=False, description="Selling price")
        renting_price = graphene.Decimal(required=False, description="Renting price")

        # Status and scheduling
        status = graphene.Boolean(required=False, description="Current status")
        renting_date = graphene.Date(required=False, description="Renting date")

        # Property description
        description = graphene.String(required=False, description="Property description")
        property_condition = graphene.String(required=False, description="Condition of the property")

        # Address information
        region = graphene.String(required=False, description="Region/state")
        district = graphene.String(required=False, description="District")
        commune = graphene.String(required=False, description="Commune/city")
        quartier = graphene.String(required=False, description="Neighborhood/quarter")
        address = graphene.String(required=False, description="Street address")

        # Relationships
        owner_id = graphene.Int(required=True, description="ID of the property owner")
        property_images = graphene.List(PropertyImageInput, required=False, description="Images of the property")
    property = graphene.Field(PropertyType, description="The newly created property")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                owner_id = kwargs.get('owner_id')
                property_images = kwargs.get('property_images', [])

                try:
                    owner = Owner.objects.get(id=owner_id)
                except Owner.DoesNotExist:
                    return AddPropertyMutation( property=None, success=False, message=f"Owner with ID {owner_id} does not exist" )

                property = Property.objects.create( name=kwargs.get('name'),region=kwargs.get('region'), district=kwargs.get('district'), commune=kwargs.get('commune'), quartier=kwargs.get('quartier'), address=kwargs.get('address'), property_type=kwargs.get('property_type'), type=kwargs.get('type'), surface=kwargs.get('surface'), room_nbr=kwargs.get('room_nbr'), bath_room_nbr=kwargs.get('bath_room_nbr'), construction_year=kwargs.get('construction_year'), selling_price=kwargs.get('selling_price'), renting_price=kwargs.get('renting_price'), status=kwargs.get('status'), renting_date=kwargs.get('renting_date'), description=kwargs.get('description'), property_condition=kwargs.get('property_condition'), owner=owner)

                for image_data in property_images:
                    PropertyImages.objects.create( description=image_data.description, property=property, image=image_data.image )

                return AddPropertyMutation( property=property, success=True, message="Property created successfully")

        except ValidationError as e:
            return AddPropertyMutation( property=None, success=False, message=f"Validation error: {str(e)}" )
        except Exception as e:
            logger.error(f"Error creating property: {str(e)}")
            return AddPropertyMutation( property=None, success=False, message=f"An error occurred: {str(e)}" )


class AddTenantMutation(graphene.Mutation):
    class Arguments:
        # Financial information
        rent_amount = graphene.Decimal(required=True, description="Monthly rent amount")
        payment_method = graphene.String(required=True, description="Method of payment")
        payment_deposit = graphene.Decimal(required=True, description="Deposit amount")
        guarantor = graphene.String(required=True, description="Guarantor information")

        # Address information
        region = graphene.String(required=True, description="Region/state")
        district = graphene.String(required=True, description="District")
        commune = graphene.String(required=True, description="Commune/city")
        quartier = graphene.String(required=True, description="Neighborhood/quarter")
        address = graphene.String(required=True, description="Street address")
        # Foreign key
        user_id = graphene.String( required=True, description="Id of the user")

    user = graphene.Field(UserType, description="The newly created User")
    tenant = graphene.Field(TenantType, description="The newly created tenant")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            # Create and save address within a transaction
            with transaction.atomic():
                User = get_user_model()
                user = User.objects.get(id=kwargs.get('user_id'))

                # Create and save tenant
                tenant = Tenant.objects.create(
                    rent_amount=kwargs.get('rent_amount'),
                    payment_method=kwargs.get('payment_method'),
                    payment_deposit=kwargs.get('payment_deposit'),
                    guarantor=kwargs.get('guarantor'),
                    region=kwargs.get('region'),
                    district=kwargs.get('district'),
                    commune=kwargs.get('commune'),
                    quartier=kwargs.get('quartier'),
                    address=kwargs.get('address')
                )
                user.objects.update(tenant = tenant)


                return AddTenantMutation( tenant=tenant, user= user, success=True, message="Tenant added successfully" )
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {kwargs.get('user_id')} does not exist.")
        except ValidationError as e:
            return AddTenantMutation( tenant=None, success=False, message=f"Validation error: {str(e)}" )
        except Exception as e:
            # logger.error(f"Error creating tenant: {str(e)}")
            return AddTenantMutation( tenant=None, success=False, message=f"An error occurred: {str(e)}" )


class AddOwnerMutation(graphene.Mutation):
    class Arguments:
        type = graphene.String(required=True, description="Type of Owner")        # Address information
        region = graphene.String(required=True, description="Region/state")
        district = graphene.String(required=True, description="District")
        commune = graphene.String(required=True, description="Commune/city")
        quartier = graphene.String(required=True, description="Neighborhood/quarter")
        address = graphene.String(required=True, description="Street address")
        # Foreign key
        user_id = graphene.String( required=True, description="Id of the user")

    # Return fields
    user = graphene.Field(UserType, description="The newly created User")
    owner = graphene.Field(OwnerType, description="The newly created owner")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                User = get_user_model()
                user = User.objects.get(id=kwargs.get('user_id'))
                # Extract foreign key IDs
                owner = Owner.objects.create(
                    type=kwargs.get('type'),
                    region=kwargs.get('region'),
                    district=kwargs.get('district'),
                    commune=kwargs.get('commune'),
                    quartier=kwargs.get('quartier'),
                    address=kwargs.get('address')
                )

                user.owner = owner
                user.save()

                return AddOwnerMutation( owner=owner, user = user, success=True, message="Owner created successfully" )
        except User.DoesNotExist:
            raise GraphQLError(f"User with ID {kwargs.get('user_id')} does not exist.")
        except ValidationError as e:
            return AddOwnerMutation( owner=None, user = None, success=False, message=f"Validation error: {str(e)}" )
        except Exception as e:
            # logger.error(f"Error creating owner: {str(e)}")
            return AddOwnerMutation( owner=None, user = None, success=False, message=f"An error occurred: {str(e)}" )


class AddPropertyImagesMutation(graphene.Mutation):
    """Mutation to add images to an existing property"""

    class Arguments:
        property_id = graphene.Int(required=True, description="ID of the property to add images to")
        images = graphene.List(PropertyImageInput, required=True, description="List of images to upload")

    # Return fields
    property_images = graphene.List(PropertyImageType, description="The newly created property images")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")

    @classmethod
    def mutate(cls, root, info, property_id, images):
        try:
            with transaction.atomic():
                # Validate property exists
                try:
                    property_obj = Property.objects.get(id=property_id)
                except Property.DoesNotExist:
                    return AddPropertyImagesMutation( property_images=None, success=False, message=f"Property with ID {property_id} does not exist" )

                created_images = []
                # Create property images
                for image_data in images:
                    property_image = PropertyImages.objects.create( description=image_data.description, image=image_data.image, property=property_obj )
                    created_images.append(property_image)
                return AddPropertyImagesMutation( property_images=created_images, success=True, message=f"Successfully added {len(created_images)} images to property" )

        except ValidationError as e:
            return AddPropertyImagesMutation( property_images=None, success=False, message=f"Validation error: {str(e)}" )
        except Exception as e:
            # logger.error(f"Error adding property images: {str(e)}")
            return AddPropertyImagesMutation( property_images=None, success=False, message=f"An error occurred: {str(e)}" )


class AddPaymentMutation(graphene.Mutation):
    """Mutation to add a new payment record"""

    class Arguments:
        amount = graphene.Decimal(required=True, description="Payment amount")
        payment_date = graphene.Date(required=True, description="Date of payment")
        payment_type = graphene.String(required=False, description="Type of payment")
        payment_method = graphene.String(required=False, description="Method of payment")
        status = graphene.String(required=False, description="Payment status")
        # Foreign keys
        tenant_id = graphene.Int(required=True, description="ID of the tenant making the payment")
        property_id = graphene.Int(required=True, description="ID of the property the payment is for")

    # Return fields
    payment = graphene.Field(PaymentType, description="The newly created payment")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                tenant_id = kwargs.get('tenant_id')
                property_id = kwargs.get('property_id')

                try:
                    tenant = Tenant.objects.get(id=tenant_id)
                except Tenant.DoesNotExist:
                    return AddPaymentMutation( payment=None, success=False, message=f"Tenant with ID {tenant_id} does not exist" )

                try:
                    property_obj = Property.objects.get(id=property_id)
                except Property.DoesNotExist:
                    return AddPaymentMutation( payment=None, success=False, message=f"Property with ID {property_id} does not exist" )

                payment = Payment.objects.create(amount=kwargs.get('amount'),payment_date=kwargs.get('payment_date'),payment_type=kwargs.get('payment_type'),payment_method=kwargs.get('payment_method'),status=kwargs.get('status'),tenant=tenant,property=property_obj)
                return AddPaymentMutation( payment=payment, success=True, message="Payment created successfully" )

        except ValidationError as e:
            return AddPaymentMutation( payment=None, success=False, message=f"Validation error: {str(e)}" )
        except Exception as e:
            # logger.error(f"Error creating payment: {str(e)}")
            return AddPaymentMutation( payment=None, success=False, message=f"An error occurred: {str(e)}" )


class AddLeaseContractMutation(graphene.Mutation):
    """Mutation to add a new lease contract"""

    class Arguments:
        name = graphene.String(required=False, description="Name of the lease contract")
        lease_start_date = graphene.Date(required=True, description="Start date of the lease")
        lease_end_date = graphene.Date(required=True, description="End date of the lease")
        rent_amount = graphene.Decimal(required=True, description="Monthly rent amount")
        contract_status = graphene.Boolean(default_value=True, description="Status of the contract")
        rules = graphene.String(required=True, description="Contract rules and conditions")
        # Foreign keys
        tenant_id = graphene.Int(required=True, description="ID of the tenant")
        property_id = graphene.Int(required=True, description="ID of the property")

    # Return fields
    lease_contract = graphene.Field(LeaseContractType, description="The newly created lease contract")
    success = graphene.Boolean(description="Whether the mutation was successful")
    message = graphene.String(description="Success or error message")

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            with transaction.atomic():
                # Extract foreign key IDs
                tenant_id = kwargs.get('tenant_id')
                property_id = kwargs.get('property_id')

                # Validate tenant exists
                try:
                    tenant = Tenant.objects.get(id=tenant_id)
                except Tenant.DoesNotExist:
                    return AddLeaseContractMutation( lease_contract=None, success=False, message=f"Tenant with ID {tenant_id} does not exist" )

                # Validate property exists
                try:
                    property_obj = Property.objects.get(id=property_id)
                except Property.DoesNotExist:
                    return AddLeaseContractMutation( lease_contract=None, success=False, message=f"Property with ID {property_id} does not exist" )

                # Validate lease dates
                lease_start_date = kwargs.get('lease_start_date')
                lease_end_date = kwargs.get('lease_end_date')
                if lease_start_date and lease_end_date and lease_start_date > lease_end_date:
                    return AddLeaseContractMutation( lease_contract=None, success=False, message="Lease start date cannot be after end date" )

                # Check if tenant or property already has an active lease
                existing_tenant_lease = LeaseContract.objects.filter(
                    tenant=tenant,
                    contract_status=True
                ).first()

                if existing_tenant_lease:
                    return AddLeaseContractMutation( lease_contract=None, success=False, message=f"Tenant already has an active lease contract (ID: {existing_tenant_lease.id})" )

                existing_property_lease = LeaseContract.objects.filter( property=property_obj, contract_status=True ).first()

                if existing_property_lease:
                    return AddLeaseContractMutation( lease_contract=None, success=False, message=f"Property already has an active lease contract (ID: {existing_property_lease.id})" )

                # Create lease contract
                lease_contract = LeaseContract.objects.create(
                    name=kwargs.get('name'),
                    lease_start_date=lease_start_date,
                    lease_end_date=lease_end_date,
                    rent_amount=kwargs.get('rent_amount'),
                    contract_status=kwargs.get('contract_status', True),
                    rules=kwargs.get('rules'),
                    tenant=tenant,
                    property=property_obj
                )

                return AddLeaseContractMutation( lease_contract=lease_contract, success=True, message="Lease contract created successfully" )

        except ValidationError as e:
            return AddLeaseContractMutation( lease_contract=None, success=False, message=f"Validation error: {str(e)}" )
        except Exception as e:
            # logger.error(f"Error creating lease contract: {str(e)}")
            return AddLeaseContractMutation( lease_contract=None, success=False, message=f"An error occurred: {str(e)}" )