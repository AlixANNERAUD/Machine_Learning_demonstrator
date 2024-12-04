from rest_framework.decorators import api_view
from django.apps import apps
import logging
import pandas
from django.core.paginator import Paginator
from django.http import JsonResponse

from . import data

configuration = apps.get_app_config("application")


@api_view(["GET"])
def tracks_view(request):
    search = request.GET.get("search", "")

    metadata = data.get_metadata()

    if search == "":
        tracks = metadata
    else:
        tracks = metadata[
            metadata["track_name"].str.contains(
                search, case=False, na=False
            )
        ]

    paginator = Paginator(tracks, 100)

    page_number = request.GET.get("page", 1)

    page = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_number

    tracks = page.object_list[
        ["release_date", "track_name", "artists", "track_duration_ms"]
    ]

    return JsonResponse(
        {
            "tracks": tracks.to_dict(orient="records", index=True),
            "total_pages": total_pages,
            "current_page": current_page,
        }
    )
