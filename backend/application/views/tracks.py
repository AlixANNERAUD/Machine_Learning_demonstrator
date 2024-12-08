from rest_framework.decorators import api_view
from django.apps import apps
import logging
import pandas
from django.core.paginator import Paginator
from django.http import JsonResponse

from . import data

CONFIGURATION = apps.get_app_config("application")

@api_view(["GET"])
def tracks_view(request):
    # Get the search query and page number from the request
    search = request.GET.get("search", "")
    page_number = request.GET.get("page", 1)

    # Do the search in a case-insensitive way if the search query is not empty
    search = search.lower()
    metadata = data.get_metadata()

    if search == "":
        tracks = metadata
    else:
        tracks = filter(
            lambda _, value: search in value["track_name"].lower(), metadata.items()
        )
        tracks = dict(tracks)

    # Paginate the results
    paginator = Paginator(tuple(tracks), 100)

    page = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_number

    print(f"Returning page {current_page} of {total_pages}")

    return JsonResponse(
        {
            "tracks": page.object_list,
            "total_pages": total_pages,
            "current_page": current_page,
        },
        safe=False,
    )
