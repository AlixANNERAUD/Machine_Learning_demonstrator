from django.urls import path

from .views.umap import umap_view
from .views.tracks import tracks_view
from .views.pca import pca_view
from .views.compose import compose_view
from .views.deezer import search_view, track_view, playlist_view
from .views.scrape import scrape_view, queues_view
from .views.genre import genre_view

urlpatterns = [
    path("tracks/", tracks_view, name="Tracks"),
    path("umap/", umap_view, name="UMAP"),
    path("pca/", pca_view, name="PCA"),
    path("compose/", compose_view, name="Compose"),
    path("scrape/", scrape_view, name="Scrape"),
    path("queues/", queues_view, name="Queues"),
    path("genre/", genre_view, name="Genre"),
    path("deezer/search/", search_view, name="Search"),
    path("deezer/track/", track_view, name="Track"),
    path("deezer/playlist/", playlist_view, name="Playlist"),
]
