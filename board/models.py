
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    board_title = models.CharField(max_length=255, verbose_name="Board Title")
    board_description = models.TextField(blank=True, null=True, verbose_name="Description")
    board_users = models.ManyToManyField(User, related_name="boards", verbose_name="Users")

    def __str__(self):
        return self.title

class Column(models.Model):
    column_board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    column_title = models.CharField(max_length=255, verbose_name="Column Title")
    column_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.board.title})"
