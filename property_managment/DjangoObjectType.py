import graphene
from graphene_django import DjangoObjectType
from property_managment.models import Property, Tenant, Payment, LeaseContract, PropertyImages, Owner


class PropertyType(DjangoObjectType):
    class Meta:
        model = Property
        fields = "__all__"


class TenantType(DjangoObjectType):
    class Meta:
        model = Tenant
        fields = "__all__"


class PaymentType(DjangoObjectType):
    class Meta:
        model = Payment
        fields = "__all__"

class LeaseContractType(DjangoObjectType):
    class Meta:
        model = LeaseContract
        fields = "__all__"


class OwnerType(DjangoObjectType):
    class Meta:
        model = Owner
        fields = "__all__"


class PropertyImageType(DjangoObjectType):
    class Meta:
        model = PropertyImages
        fields = "__all__"

    image_url = graphene.String()

    def resolve_image_url(self, info):
        if self.image:
            return info.context.build_absolute_uri(self.image.url)
        return None




