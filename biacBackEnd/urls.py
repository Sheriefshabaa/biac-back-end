
from django.contrib import admin
from django.urls import path, include
from classified_image import urls as classified_image
from users import urls as auth_urls
from image import urls as upolad_image_urls
from firstAidsProcedure import urls as firstAidsProcedure_urls
from tbsa import urls as tbsa_urls

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    path('classification/', include(classified_image)),
    path('classification/',include(upolad_image_urls)),
    path('accounts/', include('allauth.urls')),
    path('results/',include(firstAidsProcedure_urls)),
    path('tbsa/',include(tbsa_urls)),
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


