from django.urls import path

from app import views

urlpatterns = [
    # path("user/", views.user),
    path("user/", views.UserView.as_view()),
    path("users/", views.UserAPIView.as_view()),
    path("user/<str:id>/", views.UserView.as_view()),
    path("users/<str:id>/", views.UserAPIView.as_view()),
]
