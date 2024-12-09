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
    metadata = data.get_metadata().values()
    
    if search == "":
        tracks = metadata
    else:
        tracks = filter(
            lambda value: search in value["title"].lower(), metadata
        )

    # Paginate the results
    paginator = Paginator(list(tracks), 100)

    page = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_number
    
    return JsonResponse(
        {
            "tracks": page.object_list,
            "total_pages": total_pages,
            "current_page": current_page,
        },
        safe=False,
    )
