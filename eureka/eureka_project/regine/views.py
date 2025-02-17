from django.shortcuts import render, redirect, get_object_or_404
from home.models import GameBoard, CustomUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse


# Create your views here.
def regine(request):
    difficulty = request.session.get("difficulty", None)
    if difficulty == "easy":
        return render(request, "regine/regine2.html")
    elif difficulty == "hard":
        return render(request, "regine/regine1.html")
    else:
        return render(request, "regine/regine3.html")


def regine_detail(request, difficulty, game_id):
    game = get_object_or_404(GameBoard, id=game_id)

    if difficulty == "facile":
        board_size = 5
    elif difficulty == "difficile":
        board_size = 8
    else:
        board_size = 6

    context = {
        "game": game,
        "boardSize": board_size,
    }
    return render(request, "regine/regine_details.html", context)


@csrf_exempt
@login_required
@require_POST
def complete_regine(request):
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
