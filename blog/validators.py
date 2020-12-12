from django import forms
from .models import Post


def slug_validator(slug):
    try:
        p = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        p = None

    if p is not None:
        raise forms.ValidationError(
            'This slug is exist'
        )

    if slug.__contains__(' '):
        raise forms.ValidationError(
            'Slug is not valid'
        )


