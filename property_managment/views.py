import json
import logging
import re
from decimal import Decimal, InvalidOperation

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PropertySerializer, PropertyImagesSerializer
from .models import Property, PropertyImages, Owner

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

logger = logging.getLogger("django")


# Gestion des cas particuliers
@csrf_exempt
@require_http_methods('POST')
def addProperty(request):
    try:
        with (transaction.atomic()):
            if request.method == 'POST' and request.FILES['photos']:
                property = request.POST.get('property', '')
                json_property = json.loads(property)

                print(f'json_property: {json_property}')
                logger.info(f'json_property: {json_property}')
                logger.error(f'json_property: {json_property}')

                User = get_user_model()

                owner = User.objects.get(id=int(json_property['owner'])).owner

                property_ = Property(
                    name = json_property['name'],
                    announcement_type =  json_property['type'],
                    property_type = json_property['property_type'],
                    surface = json_property['surface'],
                    room_nbr = json_property['room_nbr'],
                    bath_room_nbr =   json_property['bath_room_nbr'],
                    construction_year = json_property['construction_year'],
                    selling_price = json_property['selling_price'],
                    renting_price = json_property['renting_price'],
                    status = json_property['status'],
                    renting_date = json_property['renting_date'],
                    description = json_property['description'],
                    property_condition = json_property['property_condition'],
                    region =  json_property['region'],
                    district = json_property['district'],
                    commune = json_property['commune'],
                    quartier = json_property['quartier'],
                    address = json_property['address'],
                    # Foreign key
                    owner = owner
                )
                property_.save()

                list_property_images = []
                for field_name, file_obj in request.FILES.items():
                    print(f"Champ: {field_name}, Fichier: {file_obj.name}")

                    property_images = PropertyImages(
                        image = file_obj,
                        property = property_
                    )
                    list_property_images.append(property_images)


                PropertyImages.objects.bulk_create(list_property_images)

    except Owner.DoesNotExist:
        return JsonResponse({'status': 'Error', 'message': 'Owner Does Not Exist'}, status=404)

    except Exception as e:
        print(f"Exception {str(e)}")
        raise Exception(f"Exception {str(e)}")

    return JsonResponse({'status': 'Succes', 'message': 'Property added successfully'}, status=201)

