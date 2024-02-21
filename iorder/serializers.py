from rest_framework import serializers
from iorder.models import drink

class Drinkserializer(serializers.ModelSerializer):
    class Meta:
        model = drink
        fields=['id','name']