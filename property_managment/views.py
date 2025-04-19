import re
from decimal import Decimal, InvalidOperation

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PropertySerializer, PropertyImagesSerializer
from .models import Property, PropertyImages, Owner

# Gestion des cas particuliers
