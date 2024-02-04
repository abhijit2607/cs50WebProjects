from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("home/", views.index, name="index"),
    path("search/", views.search, name="search"),    
    path("random/", views.random, name="random"),
    path("new-page/", views.new_page, name = "new-page"),
    path("<str:name>/", views.entry, name="entry"),
]
