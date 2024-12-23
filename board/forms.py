from django import forms
from .models import Board, Column
from django.contrib.auth.models import User

class BoardForm(forms.ModelForm):
    board_members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Or use forms.SelectMultiple for dropdown
        required=True,
        label="Board Members"
    )

    class Meta:
        model = Board
        fields = ['board_title', 'board_description', 'board_members']

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['column_title', 'column_order']
