from django.urls import path

from stu import views

urlpatterns = [

    path("info/", views.StudentAPIView.as_view()),
    path("info/<str:pk>/", views.StudentAPIView.as_view()),
]