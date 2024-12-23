
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Board(models.Model):
    board_title = models.CharField(max_length=255, verbose_name="Board Title")
    board_description = models.TextField(blank=True, null=True, verbose_name="Description")
    board_members = models.ManyToManyField(User, related_name="boards", verbose_name="Users")
    board_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_boards", verbose_name="Created By")
    board_created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
    
    def __str__(self):
        return self.board_title

class Column(models.Model):
    column_board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    column_title = models.CharField(max_length=255, verbose_name="Column Title")
    column_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Column"
        verbose_name_plural = "Columns"
        ordering = ["column_order"]
    
    def __str__(self):
        return f"{self.column_title} ({self.column_board.board_title})"


