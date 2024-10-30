from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sklearn.manifold import TSNE
import plotly.express as px
import umap


# Create your views here.
def tracks(request):
    tracks = settings.TRACKS

    paginator = Paginator(tracks, 100)

    page_number = request.GET.get("page")

    page = paginator.get_page(page_number)

    tracks_html = page.object_list.to_html()

    return render(request, "tracks.html", {"tracks": tracks_html, "page": page})


def tsne(request):

    tracks = settings.TRACKS[::50]

    numeric_columns = tracks.select_dtypes(include=["float64", "int64"]).dropna(axis=0)

    print(numeric_columns.info())

    tsne_results = umap.UMAP().fit_transform(numeric_columns)

    figure = px.scatter(x=tsne_results[:, 0], y=tsne_results[:, 1])

    plot_html = figure.to_html()

    return render(request, "tsne.html", {"plot": plot_html})
