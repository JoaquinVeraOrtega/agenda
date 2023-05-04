from django import forms
from django.forms import DateInput
from .models import Todo


class TodoForm(forms.ModelForm):            
    class Meta:
        model = Todo
        exclude = ('date','user',)
        widgets = {
            'estimated_end': DateInput(attrs={'type':'date'})
        }
