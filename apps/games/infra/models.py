"""
Models Django do bounded context `games`.

Mapeia fielmente docs/database-model.md:
- Game (UUID PK, igdb_id UNIQUE, ratings 0-100 com CheckConstraint)
- Genre (UUID PK, name UNIQUE)
- LibraryEntry (UUID PK, FK user CASCADE, FK game RESTRICT, UNIQUE
  (user, game) para RN01, CheckConstraint de score 1-10 e de score
  condicional ao status para RN02)

Lembrete: as CheckConstraint do Meta.constraints são a aplicação real das
regras de negócio no nível de banco — não é redundante com a validação do
use case, é uma segunda linha de defesa (defesa em profundidade).
"""

import uuid

from django.db import models
from django.db.models.functions import Length


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    igdb_genre_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    igdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(max_length=500, null=True, blank=True)
    critic_rating = models.FloatField(null=True, blank=True)
    community_rating = models.FloatField(null=True, blank=True)
    platforms = models.JSONField(default=list, blank=True)
    cached_at = models.DateTimeField()
    genres = models.ManyToManyField(Genre, related_name="games")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(critic_rating__isnull=True)
                | (models.Q(critic_rating__gte=0) & models.Q(critic_rating__lte=100)),
                name="critic_rating_range",
            ),
            models.CheckConstraint(
                check=models.Q(community_rating__isnull=True)
                | (models.Q(community_rating__gte=0) & models.Q(community_rating__lte=100)),
                name="community_rating_range",
            ),
        ]

    def __str__(self):
        return self.title


class EntryStatus(models.TextChoices):
    WANT_TO_PLAY = "want_to_play", "Want to Play"
    PLAYING = "playing", "Playing"
    COMPLETED = "completed", "Completed"
    ABANDONED = "abandoned", "Abandoned"


class LibraryEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, related_name="library_entries"
    )
    game = models.ForeignKey(
        to=Game, on_delete=models.RESTRICT, related_name="library_entries"
    )
    status = models.CharField(max_length=20, choices=EntryStatus.choices)
    score = models.SmallIntegerField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    rated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"], name="unique_user_game"),
            models.CheckConstraint(
                check=models.Q(score__isnull=True)
                | (models.Q(score__gte=1) & models.Q(score__lte=10)),
                name="score_range",
            ),
            models.CheckConstraint(
                check=~models.Q(
                    status__in=[EntryStatus.COMPLETED, EntryStatus.ABANDONED])
                | models.Q(score__isnull=False),
                name="score_required_when_finished",
            ),
            models.CheckConstraint(
                check=models.Q(review__isnull=True) | models.Q(
                    review_length__lte=8000),
                name="review_max_length",
                violation_error_message="Review não pode ultrapassar 8000 caracteres.",
            ),
        ]

    def __str__(self):
        return f"{self.user_id} — {self.game_id} ({self.status})"
