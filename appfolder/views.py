from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import ImageSerializer
from .utils import process_image
from .models import UploadedImage
import base64

class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            image_instance = UploadedImage.objects.last()
            if image_instance:
                image_data = image_instance.image.read()
                try:
                    colors, image_base64 = process_image(image_data)
                    response_data = {
                        "colors": colors,
                        "image": image_base64.decode('utf-8')
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(f"Error processing image: {e}")
                    return Response({"error": "Error processing image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "No image found in the database"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def upload_page(request):
    return render(request, 'index.html')