from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/text-to-image/', views.text_to_image, name='text_to_image'),
    path('api/image-history/', views.image_history, name='image_history'),
    
]
urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)