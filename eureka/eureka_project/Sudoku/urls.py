from django.urls import path
from . import views

app_name = "Sudoku"

urlpatterns = [
    path("", views.index, name="index"),
    path("game/<int:game_id>/", views.game_detail, name="game_detail"),
    path("complete_sudoku/", views.complete_sudoku, name="complete_sudoku"),
]
