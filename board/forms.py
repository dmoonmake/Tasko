from django import forms
from .models import Board, Column
from django.contrib.auth.models import User

class BoardForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
    class Meta:
        model = Board
        fields = ['board_title', 'board_description', 'users']

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['column_title', 'column_order']
