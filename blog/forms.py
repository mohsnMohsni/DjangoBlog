from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;',
                                                    'rows': '10', 'cols': '80',
                                                    'placeholder': 'Enter your comment...'})}
