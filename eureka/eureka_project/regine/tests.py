from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from home.models import Game, GameBoard, CustomUser

User = get_user_model()


class MyTestCase(TestCase):

    def test_regine_view(self):
        client = Client()
        response = client.get("/regine")
        self.assertEqual(response.status_code, 200)

    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpassword"
        )
        self.client.login(email="test@example.com", password="testpassword")

    def test_button_redirects_to_categorie_page_hard(self):
        client = Client()
        response = client.get(reverse("home:difficolta"))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse("home:set_difficolta", kwargs={"difficulty": "hard"})
        )
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


class RegineDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = Game.objects.create(name="Regine", game_type="regine")
        self.game_board_easy = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="facile", value_points=10
        )
        self.game_board_hard = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="difficile", value_points=20
        )
        self.game_board_medium = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="medio", value_points=15
        )

    def test_regine_detail_easy(self):
        response = self.client.get(
            reverse(
                "regine:regine_detail",
                kwargs={"difficulty": "facile", "game_id": self.game_board_easy.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "regine/regine_details.html")
        self.assertEqual(response.context["boardSize"], 5)

    def test_regine_detail_hard(self):
        response = self.client.get(
            reverse(
                "regine:regine_detail",
                kwargs={"difficulty": "difficile", "game_id": self.game_board_hard.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "regine/regine_details.html")
        self.assertEqual(response.context["boardSize"], 8)

    def test_regine_detail_medium(self):
        response = self.client.get(
            reverse(
                "regine:regine_detail",
                kwargs={"difficulty": "medio", "game_id": self.game_board_medium.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "regine/regine_details.html")
        self.assertEqual(response.context["boardSize"], 6)


class CompleteRegineViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="testuser@gmail.com", username="testuser", password="12345"
        )
        self.game = Game.objects.create(name="Regine", game_type="regine")
        self.game_board = GameBoard.objects.create(
            game=self.game, board_data={}, difficulty="facile", value_points=10
        )

    def test_complete_regine_view(self):
        self.client.login(email="testuser@gmail.com", password="12345")
        response = self.client.get(reverse("home:user_profile"))
        self.assertTrue(response)

        response = self.client.post(
            reverse("regine:complete_regine"), {"game_id": self.game_board.id}
        )
        self.assertRedirects(response, reverse("home:user_profile"))

        self.user.refresh_from_db()
        self.assertIn(self.game_board, self.user.completed_games.all())

        self.assertEqual(self.user.total_score, self.game_board.value_points)
