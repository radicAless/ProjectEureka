from django.urls import path, include
from . import views

app_name = "home"  # Define the app namespace

urlpatterns = [
    path("", views.login_view, name="login"),
    path("index/", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("difficolta", views.difficolta, name="difficolta"),
    path("categorie", views.categorie, name="categorie"),
    path(
        "set_difficoltà/<str:difficulty>/", views.set_difficolta, name="set_difficolta"
    ),
    path("game_detail/<int:game_id>/", views.game_detail, name="game_detail"),
    path("profile/", views.user_profile, name="user_profile"),
    path("filtro_giochi/", views.filtro_giochi, name="filtro_giochi"),
    path(
        "filtro_categorie/<str:game_type>/",
        views.filtro_categorie,
        name="filtro_categorie",
    ),
]
