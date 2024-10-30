from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def tracks(request):
    tracks = settings.TRACKS

    paginator = Paginator(tracks, 100)

    page_number = request.GET.get("page")

    page = paginator.get_page(page_number)

    tracks_html = page.object_list.to_html()

    return render(request, "tracks.html", {"tracks": tracks_html, "page": page})

