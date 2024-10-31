from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sklearn.manifold import TSNE
import plotly.express as px
import numpy
#import umap


# Create your views here.
def tracks_view(request):
    search = request.GET.get("search", "")
    
    if search == "":
        tracks = settings.TRACKS
    else:
        tracks = settings.TRACKS[settings.TRACKS["track_name"].str.contains(search, case=False, na=False)]

    paginator = Paginator(tracks, 100)

    page_number = request.GET.get("page", 1)

    page = paginator.get_page(page_number)

    tracks_html = page.object_list.to_html()

    return render(request, "tracks.html", {"tracks": tracks_html, "page": page, "search": search})

def umap_view(request):
    print(settings.UMAP.head())
    
    figure = px.scatter_3d(settings.UMAP[["x", "y", "z"]], x="x", y="y", z="z", color=numpy.linspace(0, 1, settings.UMAP.shape[0]))

    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    plot_html = figure.to_html(full_html=False, default_height="100%", default_width="100%")

    return render(request, "umap.html", {"plot": plot_html})
