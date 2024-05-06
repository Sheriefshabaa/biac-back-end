from django.conf import settings
from django.urls import path
from .views import classifiy_image
from django.conf.urls.static import static

urlpatterns = [
    path('classified_image/<int:id>/',classifiy_image.as_view(),name="classifiy_image")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)