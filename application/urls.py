from django.urls import path

from . import views

urlpatterns = [
    path("tracks/", views.tracks_view, name="Tracks"),
    path("umap/", views.umap_view, name="UMAP"),
]
