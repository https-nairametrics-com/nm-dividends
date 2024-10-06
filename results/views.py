from django.shortcuts import render
import csv
import json
import chardet
from io import StringIO
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import NMData
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializers import NMDataSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
# Create your views here.

@api_view(['POST'])
@permission_classes({IsAuthenticated, IsAdminUser})
def upload_csv(request):
    
    if request.method == 'POST':
        # Retrieve form data
        file = request.FILES.get('csv_file')
        name = request.data.get('name')
        data_type = request.data.get('data_type')
        description = request.data.get('description')
        upload_date = request.data.get('upload_date')
        status = request.data.get('status')

        if file:
            try:
                # Detect the encoding of the file
                raw_data = file.read(1024)  # Read first 1024 bytes for detection
                result = chardet.detect(raw_data)
                encoding = result.get('encoding')

                # Reset file pointer to the start after reading for detection
                file.seek(0)

                # If encoding is None or ascii, fall back to utf-8 and latin-1
                if not encoding or encoding.lower() == 'ascii':
                    encoding = 'utf-8'
                
                try:
                    # Try decoding using the detected or utf-8 encoding
                    decoded_file = file.read().decode(encoding).splitlines()
                except UnicodeDecodeError:
                    # If utf-8 fails, fall back to latin-1 encoding
                    file.seek(0)
                    decoded_file = file.read().decode('latin-1').splitlines()

                # Parse the CSV file
                csv_reader = csv.DictReader(decoded_file)

                # Convert CSV rows to a list of dictionaries (JSON Format)
                data_as_json = [row for row in csv_reader]

                # Save the model instance, including the user ID
                csv_upload = NMData.objects.create(
                    uploaded_by=request.user,
                    name=name,
                    description=description,
                    csv_file=file,
                    data_type=data_type,
                    upload_date=upload_date,
                    status=status,
                    json_data=data_as_json
                )

                # Serialize the response, including the CSV data and the user ID
                serializer = NMDataSerializer(csv_upload)
                return Response(serializer.data, status=HTTP_201_CREATED)

            except UnicodeDecodeError as e:
                return Response({'error': f'File encoding issue: {str(e)}'}, status=HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid request'}, status=HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_uploads(request):
    user = request.user
    uploads = NMData.objects.filter(owner=user)
    serializer = NMDataSerializer(uploads, many=True)
    return Response(serializer.data)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])  # Only authenticated users can view all uploads
def view_all_uploads(request):
    if request.method == 'GET':
        # Retrieve all CSV uploads
        name = request.query_params.get('name', None)
        data_type = request.query_params.get('data_type', None)
        company = request.query_params.get('company', None)
        csv_uploads = NMData.objects.all()

        if name:
            csv_uploads = csv_uploads.filter(name__icontains=name)
        if data_type:
            csv_uploads = csv_uploads.filter(data_type__icontains=data_type)
        # If 'company' is provided, filter manually by iterating over json_data
        '''
        if company:
            filtered_uploads = []
            for upload in csv_uploads:
                for row in upload.json_data:
                    if company.lower() in row.get('Company', '').lower():
                        filtered_uploads.append(upload)
                        break
            csv_uploads = filtered_uploads

        '''
        filtered_results = []
        if company:
        # Iterate through all NMData instances
            for upload in csv_uploads:
                matched_rows = []
                # Search within the json_data for the company
                for row in upload.json_data:
                    if company.lower() in row.get('Company', '').lower():
                        matched_rows.append(row)
                if matched_rows:
                    # Create a filtered response containing only matching rows
                    filtered_results.append({
                        'id': upload.id,
                        'name': upload.name,
                        'data_type': upload.data_type,
                        'description': upload.description,
                        'upload_date': upload.upload_date,
                        'status': upload.status,
                        'uploaded_by': upload.uploaded_by.id if upload.uploaded_by else None,
                        'filtered_json_data': matched_rows,  # Return only the matching rows
                    })
            return Response(filtered_results, status=200)
            
        # Serialize the data
        serializer = NMDataSerializer(csv_uploads, many=True)

        # Return the serialized data
        return Response(serializer.data)