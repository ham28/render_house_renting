from rest_framework import serializers
from .models import Property, PropertyImages


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ['id', 'image', 'description']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImagesSerializer(many=True)

    class Meta:
        model = Property
        fields = ['id', 'name', 'type', 'surface', 'room_nbr', 'bath_room_nbr', 'construction_year', 'selling_price',
               'renting_price', 'status', 'renting_date', 'description', 'property_condition', 'owner','images']

    def create(self, validated_data):
        # Extraction des objets B de la donnée validée
        images_data = validated_data.pop('images')

        # Création de l'ObjetA
        property = Property.objects.create(**validated_data)

        # Création des ObjetB associés
        for images in images_data:
            PropertyImages.objects.create(property=property, **images)

        return property