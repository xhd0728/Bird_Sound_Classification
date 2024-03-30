from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("api/v1/audio/", include("app01.urls")),
    path("api/v1/user/", include("user.urls"))
]
