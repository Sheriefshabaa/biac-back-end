"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from classified_image import urls as classified_image
from users import urls as auth_urls
from image import urls as upolad_image_urls
from firstAidsProcedure import urls as firstAidsProcedure_urls
from tbsa import urls as tbsa_urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    # path('', include(classification_model_urls)),
    path('classification/', include(classified_image)),
    path('classification/',include(upolad_image_urls)),
    path('accounts/', include('allauth.urls')),
    path('results/',include(firstAidsProcedure_urls)),
    path('tbsa/',include(tbsa_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


