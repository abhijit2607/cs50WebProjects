from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("home/", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("random/", views.random, name="random"),
    path("new-page/", views.new_page, name="new-page"),
    path("edit-page/", views.edit_page, name="edit-page"),
    path("save-page/", views.save_entry, name ="save-entry"),
    path("<str:name>/", views.entry, name="entry"),
]
