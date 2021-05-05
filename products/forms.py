from django import forms
from .models import Feedback

class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text', 'rate']
