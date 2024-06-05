from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageSerializer
from .utils import process_image

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            image_path = file_serializer.data['image']
            colors = process_image(image_path)
            return Response(colors, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def upload_page(request):
    return render(request, 'upload.html')