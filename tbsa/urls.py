from django.conf import settings
from django.urls import path
from .views import TbsaBasicInfoView , TbsaHandImageView , TbsaBurnImagesView,TbsaModelView
from django.conf.urls.static import static

urlpatterns = [
   path('tbsa_basic_info/',TbsaBasicInfoView.as_view(),name="TbsaBasicInfoView"),
   path('tbsa_hand_image/<int:id>/',TbsaHandImageView.as_view(),name="TbsaHandimageview"),
   path('tbsa_burn_images/<int:id>/',TbsaBurnImagesView.as_view(),name="TbsaBurnImagesView"),
   path('tbsa_model/<int:tbsa_id>/<int:hand_id>/<int:burn_last_image_id>/',TbsaModelView.as_view(),name="TbsaModelView"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)