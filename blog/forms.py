from django import forms
from .models import Comment, Post
from .validators import slug_validator


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.Textarea(
            attrs={'class': 'form-control', 'style': 'resize:none;',
                   'rows': '10', 'cols': '80',
                   'placeholder': 'Enter your comment...'}
        )}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'category', 'content',
                  'draft', 'publish_time', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'slug': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'content': forms.Textarea(attrs={'class': 'form-control mb-3', 'cols': 90,
                                             'style': 'resize:none'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-control mb-3'}),
            'publish_time': forms.SelectDateWidget(attrs={'class': 'form-control mb-3'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file mb-3'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        slug_validator(slug)
        return slug


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'slug',
                  'draft', 'publish_time')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'content': forms.Textarea(attrs={'class': 'form-control mb-3', 'cols': 90,
                                             'style': 'resize:none'}),
            'draft': forms.CheckboxInput(attrs={'class': 'form-control mb-3'}),
            'publish_time': forms.SelectDateWidget(attrs={'class': 'form-control mb-3'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        slug_validator(slug)
        return slug
