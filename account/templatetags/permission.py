from django import template

register = template.Library()


@register.filter(name='is_author')
def is_author(user):
    return user.groups.filter(name='author').exists()
