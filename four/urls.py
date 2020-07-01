from django.urls import path

from four import views

urlpatterns = [
    path("bs/", views.BookAPIView.as_view()),
    path("bs/<str:id>/", views.BookAPIView.as_view()),
    path("bgs/", views.BookGenericAPIView.as_view()),
    path("bgs/<str:id>/", views.BookGenericAPIView.as_view()),
    path("bgn/", views.BookGenericAPIView.as_view()),
    path("bgn/<str:id>/", views.BookGenericAPIView.as_view()),
    path("set/", views.BookGenericViewSet.as_view({"post": "user_login", "get": "get_user_count"})),
    path("set/<str:id>/", views.BookGenericViewSet.as_view({"post": "user_login"})),

]
