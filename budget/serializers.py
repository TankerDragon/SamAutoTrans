from pyexpat import model
#from attr import field
from rest_framework import serializers
from .models import Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

    # def create(self, validated_data):
    #     log = Logs(**validated_data)
    #     log.other = 1
    #     log.save()
    #     return log

    # def update(self, insatnce, validated_data):
    #     insatnce.notes = validated_data.get('notes')
    #     insatnce.save()
    #     return insatnce
