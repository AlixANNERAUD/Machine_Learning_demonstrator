from django.urls import path

from . import views

urlpatterns = [
    path("spotify/", views.spotify_view, name="Spotify"),
    path("tracks/", views.tracks_view, name="Tracks"),
    path("umap/", views.umap_view, name="UMAP"),
    path("account/", views.account_view, name="Account"),
]
