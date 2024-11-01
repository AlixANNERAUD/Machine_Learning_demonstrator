from django.shortcuts import render
from django.http import HttpResponse
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import plotly.express as px
import numpy

configuration = apps.get_app_config("application")


# Create your views here.
def tracks_view(request):
    search = request.GET.get("search", "")

    if search == "":
        tracks = configuration.tracks
    else:
        tracks = configuration.tracks[
            configuration.tracks["track_name"].str.contains(
                search, case=False, na=False
            )
        ]

    paginator = Paginator(tracks, 100)

    page_number = request.GET.get("page", 1)

    page = paginator.get_page(page_number)

    tracks_html = page.object_list.to_html()

    return render(
        request, "tracks.html", {"tracks": tracks_html, "page": page, "search": search}
    )


def umap_view(request):
    figure = px.scatter_3d(
        configuration.umap[["x", "y", "z"]],
        x="x",
        y="y",
        z="z",
        color=numpy.linspace(0, 1, configuration.umap.shape[0]),
    )

    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    plot_html = figure.to_html(
        full_html=False, default_height="100%", default_width="100%"
    )

    return render(request, "umap.html", {"plot": plot_html})
