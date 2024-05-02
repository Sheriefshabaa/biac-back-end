from django.conf import settings
from django.urls import path, include
from classification_model.views import (ImageProcessingView)
from rest_framework import routers
from django.conf.urls.static import static

router = routers.DefaultRouter()
urlpatterns = [
    path('api/', include(router.urls)),
    path('classfication/',ImageProcessingView.as_view(),name="classficationBurn")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)