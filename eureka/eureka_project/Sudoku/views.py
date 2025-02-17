from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from home.models import GameBoard, CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    difficulty = request.session.get("difficulty", None)

    context = {
        "difficulty": difficulty,
    }
    return render(request, "Sudoku/index.html", context)


def game_detail(request, game_id):
    game = get_object_or_404(GameBoard, id=game_id)
    context = {"game": game}
    return render(request, "Sudoku/game_detail.html", context)


@csrf_exempt
@login_required
@require_POST
def complete_sudoku(request):
    game_id = request.POST.get("game_id")
    user = request.user
    print(f"Completato gioco {game_id} per l'utente {user}")
    game_board = get_object_or_404(GameBoard, id=game_id)
    user_profile = get_object_or_404(CustomUser, id=user.id)

    if game_board not in user_profile.completed_games.all():
        print(f"punteggio prima: {user_profile.total_score}")
        user_profile.completed_games.add(game_board)
        print(f"punteggio gioco: {game_board.value_points}")
        user_profile.save()
    print(f"Punteggio aggiornato a {user_profile.total_score}")
    return redirect("home:user_profile")
