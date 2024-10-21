from django.shortcuts import render
import csv
import json
import chardet
from io import StringIO
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import NMData
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .serializers import NMDataSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
# Create your views here.

@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only admins can upload and update
def upload_csv(request, pk=None):
    if request.method == 'POST':
        # Handle CSV upload (create)
        return handle_upload(request)

    elif request.method in ['PUT', 'PATCH'] and pk is not None:
        # Handle CSV update (update)
        return handle_update(request, pk)

    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


def handle_upload(request):
    """
    Handles the CSV upload creation process.
    """
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

    return Response({'error': 'CSV file is required'}, status=HTTP_400_BAD_REQUEST)


def handle_update(request, pk):
    """
    Handles the CSV upload update process.
    """
    try:
        # Find the existing NMData record by id (pk)
        csv_upload = NMData.objects.get(pk=pk)
    except NMData.DoesNotExist:
        return Response({"error": "Upload not found"}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve form data
    file = request.FILES.get('csv_file')
    name = request.data.get('name', csv_upload.name)
    data_type = request.data.get('data_type', csv_upload.data_type)
    description = request.data.get('description', csv_upload.description)
    upload_date = request.data.get('upload_date', csv_upload.upload_date)
    status = request.data.get('status', csv_upload.status)

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
            csv_upload.json_data = data_as_json  # Update json_data with the new file
            csv_upload.csv_file = file  # Update file field

        except UnicodeDecodeError as e:
            return Response({'error': f'File encoding issue: {str(e)}'}, status=HTTP_400_BAD_REQUEST)

    # Update the other fields
    csv_upload.name = name
    csv_upload.data_type = data_type
    csv_upload.description = description
    csv_upload.upload_date = upload_date
    csv_upload.status = status
    csv_upload.save()

    # Serialize and return the updated record
    serializer = NMDataSerializer(csv_upload)
    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_uploads(request):
    user = request.user
    uploads = NMData.objects.filter(owner=user)
    serializer = NMDataSerializer(uploads, many=True)
    return Response(serializer.data)

class NMDataPagination(PageNumberPagination):
    page_size = 10  # Define the number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
#@permission_classes([IsAuthenticated])  # Only authenticated users can view all uploads
def view_all_uploads(request):
    if request.method == 'GET':
        # Retrieve all CSV uploads
        name = request.query_params.get('name', None)
        data_type = request.query_params.get('data_type', None)
        company = request.query_params.get('company', None)
        csv_uploads = NMData.objects.all()
        # Filter NMData objects by 'name' and 'data_type'
        uploads = NMData.objects.all()

        if name:
                uploads = uploads.filter(name__icontains=name)

        if data_type:
            uploads = uploads.filter(data_type__icontains=data_type)

        # Sorting
        sort_by = request.query_params.get('sort_by', '-upload_date')
        uploads = uploads.order_by(sort_by)

        # Pagination using PageNumberPagination
        paginator = NMDataPagination()
        paginated_uploads = paginator.paginate_queryset(uploads, request)   

        # Prepare a list to hold the final filtered results
        filtered_results = []

        for upload in paginated_uploads:
            if company:
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
            else:
                # If no company filter, return all json_data
                filtered_results.append({
                    'id': upload.id,
                    'name': upload.name,
                    'data_type': upload.data_type,
                    'description': upload.description,
                    'upload_date': upload.upload_date,
                    'status': upload.status,
                    'uploaded_by': upload.uploaded_by.id if upload.uploaded_by else None,
                    'json_data': upload.json_data,  # Return full json_data
                })

        # Return paginated response with next and previous links
        return paginator.get_paginated_response(filtered_results)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsAdminUser])  # Only admins can update uploads
def update_upload(request, pk):
    try:
        # Find the NMData object by primary key (id)
        upload = NMData.objects.get(pk=pk)
    except NMData.DoesNotExist:
        return Response({"error": "Upload not found"}, status=status.HTTP_404_NOT_FOUND)

    # For PUT requests, update all fields. For PATCH, update only the provided fields.
    if request.method in ['PUT', 'PATCH']:
        data = request.data.copy()  # Copy request data so we can modify it
        file = request.FILES.get('csv_file')  # Handle file update

        if file:
            # Read and parse the new CSV file if provided
            try:
                decoded_file = file.read().decode('utf-8-sig').splitlines()  # Handle encoding
                csv_reader = csv.DictReader(decoded_file)
                data_as_json = [row for row in csv_reader]
                data['json_data'] = data_as_json  # Update json_data
                data['csv_file'] = file  # Update file field
            except Exception as e:
                return Response({"error": f"File encoding issue: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the rest of the fields using the serializer
        serializer = NMDataSerializer(upload, data=data, partial=True)  # partial=True allows for partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
