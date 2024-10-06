from rest_framework import serializers
from .models import NMData

class NMDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NMData
        fields = ['name', 'slug', 'data_type', 'description', 'upload_date', 'csv_file', 'json_data', 'status', 'updated_at']
