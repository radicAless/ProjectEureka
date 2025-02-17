from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Game, GameBoard


# @admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Game, GameAdmin)


# @admin.register(GameBoard)
class GameBoardAdmin(admin.ModelAdmin):
    list_display = ("game", "difficulty", "value_points")
    search_fields = ("game__name", "difficulty")
    ordering = ("game",)


admin.site.register(GameBoard, GameBoardAdmin)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "total_score",
    )
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "total_score", "completed_games")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions", "completed_games")


admin.site.register(CustomUser, CustomUserAdmin)
