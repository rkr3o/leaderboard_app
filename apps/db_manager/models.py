from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    join_date = models.DateTimeField()

    class Meta:
        db_table = 'user'

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    score = models.IntegerField()
    game_mode = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    class Meta:
        db_table = 'gamesession'
        indexes = [
            models.Index(fields=['user']),
        ]


class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id', unique=True)
    total_score = models.IntegerField()
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'leaderboard'
