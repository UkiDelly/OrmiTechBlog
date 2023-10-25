from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from myblog import settings

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL)
