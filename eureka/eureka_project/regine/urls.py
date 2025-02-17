from django.urls import path
from . import views

app_name = "regine"  # Define the app namespace

urlpatterns = [
    path("", views.regine, name="regine"),
    path(
        "regine_detail/<str:difficulty>/<int:game_id>/",
        views.regine_detail,
        name="regine_detail",
    ),
    path("complete_regine/", views.complete_regine, name="complete_regine"),
]
