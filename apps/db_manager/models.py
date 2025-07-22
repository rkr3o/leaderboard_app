from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    join_date = models.DateTimeField()

    class Meta:
        db_table = "user"


class UserDetails(models.Model):
    phone_number = models.CharField(max_length=255, unique=True)
    user_id = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_details"


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    score = models.IntegerField()
    game_mode = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "gamesession"
        indexes = [
            models.Index(fields=["user"]),
        ]


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # defaults to user_id column
    total_score = models.IntegerField()
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "leaderboard"


class JWTToken(models.Model):
    user_id = models.BigIntegerField()
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "jwt_tokens"
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["token"]),
            models.Index(fields=["is_active"]),
        ]
