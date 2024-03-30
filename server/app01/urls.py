from django.urls import path

from . import views

urlpatterns = [
    path("upload", views.AudioUploadView.as_view()),
    path("audioB64", views.AudioEncodingView.as_view()),
    path("imageB64", views.ImageEncodingView.as_view()),
    path("log", views.UploadLoggingView.as_view()),
    path("info", views.BirdInfoView.as_view()),
]
