from pyexpat import model
#from attr import field
from rest_framework import serializers
from .models import Driver, Log


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class LogSerializer (serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(
        queryset = Driver.objects.all()
    )
    # change = serializers.SerializerMethodField(method_name="calculate_change")

    class Meta:
        model = Log
        fields = ['change', 'budget_type', 'pcs_number', 'bol_number', 'user', 'note', 'driver', 'current_rate', 'original_rate', 'total_miles']


    # def create(self, validated_data):
    #     log = Logs(**validated_data)
    #     log.other = 1
    #     log.save()
    #     return log

    # def update(self, insatnce, validated_data):
    #     insatnce.notes = validated_data.get('notes')
    #     insatnce.save()
    #     return insatnce
