from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import DownloadResultsAsPDFView, ShowResultView

urlpatterns = [
                  path('show_result/<int:id>/', ShowResultView.as_view(), name="show_result"),
                  path('download_result/<int:id>/', DownloadResultsAsPDFView.as_view(), name="download_result")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
