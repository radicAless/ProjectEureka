from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import CustomUser, GameBoard


# Create your views here.
def index(request):
    top_users = CustomUser.objects.order_by("-total_score")[:3]
    users = CustomUser.objects.order_by("-total_score")[:10]
    context = {
        "users": users,
        "top_users": top_users,
    }

    return render(request, "home/index.html", context)


def set_difficolta(request, difficulty):
    request.session["difficulty"] = difficulty
    return redirect("home:filtro_giochi")


def categorie(request):
    return render(request, "home/categorie.html")


def difficolta(request):
    return render(request, "home/difficolta.html")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home:index")  # Redirect to home page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "home/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home:index")  # Redirect to home page after registration
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "home/register.html", {"form": form})


def logout_view(request):
    return auth_views.LogoutView.as_view(next_page="home:login")(request)


@login_required
def user_profile(request):
    user = request.user
    # all_games = GameBoard.objects.all()
    # completed_games = user.completed_games.all()
    all_games = GameBoard.objects.all().order_by("game__game_type", "difficulty")
    completed_games = user.completed_games.all()

    context = {
        "user": user,
        "all_games": all_games,
        "completed_games": completed_games,
    }

    return render(request, "home/user_profile.html", context)


def game_detail(request, game_id):
    game_board = get_object_or_404(GameBoard, id=game_id)
    difficulty = game_board.difficulty
    game_type = game_board.game.game_type

    if game_type == "sudoku":
        return redirect("Sudoku:game_detail", game_id=game_id)
    elif game_type == "regine":
        return redirect("regine:regine_detail", difficulty=difficulty, game_id=game_id)
    else:
        return redirect("home:index")


def filtro_giochi(request):
    user = request.user
    difficulty = request.session.get("difficulty")
    if not difficulty:
        return redirect(
            "home:index"
        )  # Redirect to home page if no difficulty is set in session
    completed_games = user.completed_games.all()

    games = GameBoard.objects.filter(difficulty=difficulty).order_by(
        "game__game_type", "difficulty"
    )
    grouped_games = {}

    for game in games:
        if game.game.name not in grouped_games:
            grouped_games[game.game.name] = []
        grouped_games[game.game.name].append(game)

    context = {
        "difficulty": difficulty,
        "grouped_games": grouped_games,
        "completed_games": completed_games,
    }
    return render(request, "home/filtro_giochi.html", context)


def filtro_categorie(request, game_type):
    user = request.user
    games = GameBoard.objects.filter(game__game_type=game_type).order_by("difficulty")
    grouped_games = {"facile": [], "medio": [], "difficile": []}
    completed_games = user.completed_games.all()

    for game in games:
        if game.difficulty in grouped_games:
            grouped_games[game.difficulty].append(game)

    sorted_grouped_games = [
        (difficulty, grouped_games[difficulty])
        for difficulty in ["facile", "medio", "difficile"]
    ]

    context = {
        "game_type": game_type,
        "grouped_games": sorted_grouped_games,
        "completed_games": completed_games,
    }
    return render(request, "home/filtro_categorie.html", context)
