from django.urls import path

from .views.umap import umap_view
from .views.tracks import tracks_view
from .views.pca import pca_view
from .views.compose import compose_view

urlpatterns = [
    path("tracks/", tracks_view, name="Tracks"),
    path("umap/", umap_view, name="UMAP"),
    path("pca/", pca_view, name="PCA"),
    path("compose/", compose_view, name="Compose"),
]
