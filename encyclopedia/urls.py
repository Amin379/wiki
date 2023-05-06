from django.urls import path
# from .util import random
from . import views

# randomTitle = random()

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title , name="title"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
    path("new_page", views.newPage, name="new_page"),
    path("edit_page/<str:title>", views.editPage, name="edit_page")

]