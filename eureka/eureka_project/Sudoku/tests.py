from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from home.models import Game, GameBoard, CustomUser

User = get_user_model()


class MyTestCase(TestCase):

    def test_Sudoku_view(self):
        client = Client()
        response = client.get("/Sudoku/")
        self.assertEqual(response.status_code, 200)

    def test_Sudoku_view_with_difficulty(self):
        client = Client()
        # Imposta la sessione con una difficoltà
        session = client.session
        session["difficulty"] = "easy"
        session.save()

        response = client.get("/Sudoku/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Difficoltà: easy")

    def test_Sudoku_view_without_difficulty(self):
        client = Client()
        response = client.get("/Sudoku/")
        session = client.session
        session.pop("difficulty", None)
        session.save()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Difficoltà: facile")

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword"
        )
        self.client.login(email="test@example.com", password="testpassword")

    def test_button_redirects_to_categorie_page_hard(self):
        # Simula una richiesta GET alla pagina in cui si trova il pulsante
        client = Client()
        response = client.get(reverse("home:difficolta"))

        # Verifica che la risposta HTTP sia 200 OK
        self.assertEqual(response.status_code, 200)

        # Verifica funzionamento pulsante difficile
        response = self.client.get(
            reverse("home:set_difficolta", kwargs={"difficulty": "hard"})
        )

        # Verifica che la risposta sia un redirect codice 302
        self.assertRedirects(response, reverse("home:filtro_giochi"))

    def test_button_redirects_to_categorie_page_medium(self):
        client = Client()
        response = client.get(reverse("home:difficolta"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse("home:set_difficolta", kwargs={"difficulty": "medium"})
        )
        self.assertRedirects(response, reverse("home:filtro_giochi"))

    def test_button_redirects_to_categorie_page_easy(self):
        client = Client()
        response = client.get(reverse("home:difficolta"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse("home:set_difficolta", kwargs={"difficulty": "easy"})
        )
        self.assertRedirects(response, reverse("home:filtro_giochi"))


class GameDetailViewTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(name="Sudoku", game_type="sudoku")
        self.game_board = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="easy", value_points=10
        )

    def test_game_detail_view(self):
        client = Client()
        response = client.get(reverse("Sudoku:game_detail", args=[self.game_board.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Sudoku/game_detail.html")
        self.assertContains(response, self.game_board.game.name)
        self.assertContains(response, self.game_board.difficulty)


class CompleteSudokuViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com", username="testuser", password="12345"
        )
        self.game = Game.objects.create(name="Sudoku", game_type="sudoku")
        self.game_board = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="easy", value_points=10
        )

    def test_complete_sudoku_view(self):

        self.client.login(email="testuser@gmail.com", password="12345")
        response = self.client.get(reverse("home:user_profile"))
        self.assertTrue(response)

        response = self.client.post(
            reverse("Sudoku:complete_sudoku"), {"game_id": self.game_board.id}
        )
        self.assertRedirects(response, reverse("home:user_profile"))

        self.user.refresh_from_db()
        self.assertIn(self.game_board, self.user.completed_games.all())

        self.assertEqual(self.user.total_score, self.game_board.value_points)
