from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.db.models.signals import m2m_changed


class Game(models.Model):
    name = models.CharField(max_length=100)
    game_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class GameBoard(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE
    )  # Add a foreign key to Game
    board_data = models.JSONField()
    difficulty = models.CharField(max_length=50)
    value_points = models.IntegerField()

    def __str__(self):
        return f"{self.game.name} - {self.difficulty}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.date_joined = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    total_score = models.IntegerField(default=0)
    completed_games = models.ManyToManyField(GameBoard, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username


def update_total_score(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.total_score = sum(
            game.value_points for game in instance.completed_games.all()
        )
        instance.save()


m2m_changed.connect(update_total_score, sender=CustomUser.completed_games.through)


class Leaderboard(models.Model):
    user = models.OneToOneField(
        "CustomUser", on_delete=models.CASCADE, related_name="leaderboard_entry"
    )
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"
