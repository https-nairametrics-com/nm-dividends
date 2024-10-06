from rest_framework import serializers
from .models import NMData

class NMDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NMData
        fields = ['id', 'uploaded_by', 'name', 'slug', 'data_type', 'description', 'upload_date', 'csv_file', 'json_data', 'status', 'updated_at']
        #depth = 1 # This will show the user details (not just the user ID)


class AdminNMDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NMData
        fields = ['id', 'uploaded_by', 'name', 'slug', 'data_type', 'description', 'upload_date', 'csv_file', 'json_data', 'status', 'updated_at']
        depth = 1 # This will show the user details (not just the user ID)
