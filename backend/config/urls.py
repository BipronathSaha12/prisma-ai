from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from images.views import HealthView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", HealthView.as_view(), name="health"),
    path("api/auth/", include("accounts.urls")),
    path("api/images/", include("images.urls")),
]

from django.urls import re_path
from django.views.static import serve

# For a Render deployment without Nginx or S3, we must serve media files through Django.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
