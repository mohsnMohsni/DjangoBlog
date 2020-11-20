from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . import models


def home(request):
  posts = models.Post.objects.all()
  string = ',\n'.join([post.title for post in posts])
  to_html = f"<html><h1>{string}</h1></html>"
  return HttpResponse(to_html)


def single(request, slug):
  post = get_object_or_404(models.Post, slug=slug)
  to_html = f"<html><h1>{post.title}</h1><br/></html>"
  return HttpResponse(to_html)