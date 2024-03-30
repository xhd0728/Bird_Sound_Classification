from django.urls import path
from . import views

urlpatterns = [
    path("email", views.EmailView.as_view()),
    path("register", views.RegisterView.as_view()),
    path("login", views.UsersView.as_view()),
]
