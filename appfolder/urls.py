from django.urls import path
from .views import ImageUploadView,upload_page

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('', upload_page, name='upload-page')
]