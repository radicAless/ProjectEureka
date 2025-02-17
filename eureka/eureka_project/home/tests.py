from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from home.models import GameBoard, Game


class MyTestCase(TestCase):

    def test_difficolta(self):
        client = Client()
        response = client.get("/difficolta")
        self.assertEqual(response.status_code, 200)

    def test_categorie(self):
        client = Client()
        response = client.get("/categorie")
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        client = Client()
        response = client.get("")
        self.assertEqual(response.status_code, 200)

    def test_categorie_link(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a href="{}" class="w3-bar-item w3-button">CATEGORIE</a>'.format(
                reverse("home:categorie")
            ),
        )

    def test_difficoltà_link(self):
        response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="{}" onclick="w3_close()" class="w3-bar-item w3-button">DIFFICOLTÀ</a>'.format(reverse("home:difficolta")))

    def test_home_link(self):
        response = self.client.get(reverse("home:difficolta"))
        self.assertEqual(response.status_code, 200)
        # controllo che nella risposta sia contenuto anche il link seguente
        self.assertContains(
            response,
            '<a href="{}" onclick="w3_close()" class="w3-bar-item w3-button"> HOME</a>'.format(
                reverse("home:index")
            ),
        )

    def test_from_categorie_to_regine_view(self):
        client = Client()
        response = client.get("/categorie")
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "home/categorie.html")
        response = client.get(reverse("regine:regine"))
        self.assertEqual(response.status_code, 200)

    def test_from_categorie_to_Sudoku_view(self):
        client = Client()
        response = client.get("/categorie")
        self.assertEqual(response.status_code, 200)
        # controllo che il template "home/categorie.html" utilizzato per generare la risposta
        self.assertTemplateUsed(response, "home/categorie.html")

        # Simula il click su un link che reindirizza alla pagina Sudoku
        response = client.get(reverse("Sudoku:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Sudoku/index.html")


class login_register(TestCase):

    def test_login_view(self):
        client = Client()
        response = client.get(reverse("home:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/login.html")

    def test_login_view_second_link(self):
        client = Client()
        response = client.get(reverse("home:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/login.html")

    def test_from_login_to_register_view(self):
        client = Client()
        response = client.get(reverse("home:login"))
        self.assertEqual(response.status_code, 200)
        # Simula click link register
        response = client.get(reverse("home:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/register.html")

    def test_register_view(self):
        client = Client()
        response = client.get(reverse("home:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/register.html")

    def test_from_register_to_login_view(self):
        client = Client()
        response = client.get(reverse("home:register"))
        self.assertEqual(response.status_code, 200)
        # simula click link register
        response = client.get(reverse("home:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/login.html")


class GameModelTest(TestCase):

    def setUp(self):
        self.game = Game.objects.create(name="Checkers", game_type="Board Game")

    def test_game_creation(self):
        self.assertIsInstance(self.game, Game)
        self.assertEqual(self.game.__str__(), "Checkers")

    def test_game_str_representation(self):
        self.assertEqual(str(self.game), "Checkers")


class GameBoardModelTest(TestCase):

    def setUp(self):
        self.game = Game.objects.create(name="Checkers", game_type="Board Game")

        self.medium_game_board = GameBoard.objects.create(
            game=self.game,
            board_data={"pieces": "initial setup"},
            difficulty="Medio",
            value_points=100,
        )
        self.easy_game_board = GameBoard.objects.create(
            game=self.game,
            board_data={"pieces": "initial setup"},
            difficulty="Facile",
            value_points=50,
        )

        self.difficult_game_board = GameBoard.objects.create(
            game=self.game,
            board_data={"pieces": "initial setup"},
            difficulty="Difficile",
            value_points=200,
        )

    def test_medium_game_board_creation(self):
        self.assertIsInstance(self.medium_game_board, GameBoard)
        self.assertEqual(self.medium_game_board.game, self.game)
        self.assertEqual(self.medium_game_board.board_data, {"pieces": "initial setup"})
        self.assertEqual(self.medium_game_board.difficulty, "Medio")
        self.assertEqual(self.medium_game_board.value_points, 100)

    def test_medium_game_board_str_representation(self):
        self.assertEqual(str(self.medium_game_board), "Checkers - Medio")

    def test_easy_game_board_creation(self):
        self.assertIsInstance(self.easy_game_board, GameBoard)
        self.assertEqual(self.easy_game_board.game, self.game)
        self.assertEqual(self.easy_game_board.board_data, {"pieces": "initial setup"})
        self.assertEqual(self.easy_game_board.difficulty, "Facile")
        self.assertEqual(self.easy_game_board.value_points, 50)

    def test_easy_game_board_str_representation(self):
        self.assertEqual(str(self.easy_game_board), "Checkers - Facile")

    def test_difficult_game_board_creation(self):
        self.assertIsInstance(self.difficult_game_board, GameBoard)
        self.assertEqual(self.difficult_game_board.game, self.game)
        self.assertEqual(
            self.difficult_game_board.board_data, {"pieces": "initial setup"}
        )
        self.assertEqual(self.difficult_game_board.difficulty, "Difficile")
        self.assertEqual(self.difficult_game_board.value_points, 200)

    def test_difficult_game_board_str_representation(self):
        self.assertEqual(str(self.difficult_game_board), "Checkers - Difficile")


class UserProfileViewTests(TestCase):

    def user_profile_view(self):
        client = Client()
        response = client.get(reverse("home:user_profile"))
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com", username="testuser", password="12345"
        )

        self.game1 = Game.objects.create(name="Game 1", game_type="Puzzle")
        self.game2 = Game.objects.create(name="Game 2", game_type="Strategy")

        self.board1 = GameBoard.objects.create(
            game=self.game1, board_data={}, difficulty="easy", value_points=10
        )
        self.board2 = GameBoard.objects.create(
            game=self.game2, board_data={}, difficulty="medium", value_points=20
        )

        self.user.completed_games.add(self.board1)

    def test_user_profile_view_redirect_if_not_logged_in(self):
        client = Client()
        response = client.get(reverse("home:user_profile"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_user_profile_view_logged_in(self):
        client = Client()
        client.login(email="testuser@gmail.com", password="12345")
        response = client.get(reverse("home:user_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/user_profile.html")
        self.assertEqual(response.context["user"], self.user)
        self.assertQuerySetEqual(
            response.context["all_games"].order_by("id"),
            GameBoard.objects.all().order_by("id"),
            transform=lambda x: x,
        )
        self.assertQuerySetEqual(
            response.context["completed_games"].order_by("id"),
            self.user.completed_games.all().order_by("id"),
            transform=lambda x: x,
        )


class GameDetailViewTest(TestCase):
    def setUp(self):
        self.sudoku_game = Game.objects.create(name="Sudoku", game_type="sudoku")
        self.regine_game = Game.objects.create(name="Regine", game_type="regine")

        self.sudoku_board = GameBoard.objects.create(
            game=self.sudoku_game, board_data={}, difficulty="easy", value_points=50
        )
        self.regine_board = GameBoard.objects.create(
            game=self.regine_game, board_data={}, difficulty="medium", value_points=100
        )

    def test_redirect_sudoku_game(self):
        response = self.client.get(
            reverse("home:game_detail", args=[self.sudoku_board.id])
        )
        self.assertRedirects(
            response, reverse("Sudoku:game_detail", args=[self.sudoku_board.id])
        )

    def test_redirect_regine_game(self):
        response = self.client.get(
            reverse("home:game_detail", args=[self.regine_board.id])
        )


User = get_user_model()


class FiltroCategorieViewTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword"
        )

        self.game = Game.objects.create(name="Test Sudoku", game_type="sudoku")
        self.game_board_easy = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="facile", value_points=10
        )
        self.game_board_hard = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="difficile", value_points=20
        )

        self.user.completed_games.add(self.game_board_easy)

    def test_filtro_categorie_view(self):

        self.client.login(email="test@example.com", password="testpassword")

        response = self.client.get(reverse("home:filtro_categorie", args=["sudoku"]))

        self.assertEqual(response.status_code, 200)

        # Verificare che il template corretto sia utilizzato
        self.assertTemplateUsed(response, "home/filtro_categorie.html")

        self.assertIn("game_type", response.context)
        self.assertIn("grouped_games", response.context)
        self.assertIn("completed_games", response.context)

        # Verificare che i dati nel contesto siano corretti
        self.assertEqual(response.context["game_type"], "sudoku")
        self.assertTrue(any(difficulty == "facile" for difficulty, _ in response.context["grouped_games"]))
        self.assertTrue(any(difficulty == "difficile" for difficulty, _ in response.context["grouped_games"]))
        facile_games = [games for difficulty, games in response.context["grouped_games"] if difficulty == "facile"]
        self.assertEqual(len(facile_games), 1)
        difficile_games = [games for difficulty, games in response.context["grouped_games"] if difficulty == "difficile"]
        self.assertEqual(len(difficile_games), 1)
        self.assertIn(self.game_board_easy, response.context["completed_games"])
        self.assertNotIn(self.game_board_hard, response.context["completed_games"])


User = get_user_model()


class FiltroGiochiViewTest(TestCase):

    def setUp(self):

        self.client = Client()

        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword"
        )

        self.client.login(email="test@example.com", password="testpassword")

        self.game1 = Game.objects.create(name="Sudoku", game_type="sudoku")
        self.game2 = Game.objects.create(name="Regine", game_type="regine")
        self.game_board_easy = GameBoard.objects.create(
            game=self.game1, board_data={}, difficulty="facile", value_points=10
        )
        self.game_board_hard = GameBoard.objects.create(
            game=self.game2, board_data={}, difficulty="difficile", value_points=20
        )

        self.user.completed_games.add(self.game_board_easy)

        session = self.client.session
        session["difficulty"] = "difficile"
        session.save()

    def test_filtro_giochi_view_with_difficulty(self):

        response = self.client.get(reverse("home:filtro_giochi"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "home/filtro_giochi.html")

        self.assertIn("difficulty", response.context)
        self.assertIn("grouped_games", response.context)
        self.assertIn("completed_games", response.context)

        self.assertEqual(response.context["difficulty"], "difficile")
        self.assertIn(self.game2.name, response.context["grouped_games"])
        self.assertEqual(len(response.context["grouped_games"][self.game2.name]), 1)
        self.assertIn(self.game_board_easy, response.context["completed_games"])

    def test_filtro_giochi_view_without_difficulty(self):
        # Rimuozione della difficoltà dalla sessione
        session = self.client.session
        session["difficulty"] = ""
        session.save()

        response = self.client.get(reverse("home:filtro_giochi"))

        # Verificare che la risposta sia un redirect alla home page
        self.assertRedirects(response, reverse("home:index"))
