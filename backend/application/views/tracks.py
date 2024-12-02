from rest_framework.decorators import api_view
from django.apps import apps
import logging
import pandas
from django.core.paginator import Paginator
from django.http import JsonResponse

configuration = apps.get_app_config("application")

tracks = None

def get_tracks():
    global tracks

    if tracks is None:
        tracks = load_tracks(f"{configuration.data_path}/tracks.csv")
        print(tracks.info)

    return tracks

def load_tracks(path: str):
    logging.info("Loading tracks ...")
    try:
        tracks = pandas.read_csv(path)
        tracks.dropna(inplace=True)
        return tracks
    except FileNotFoundError:
        logging.error("Tracks file not found")
        raise FileNotFoundError
    except Exception as e:
        logging.error(f"Error loading tracks: {e}")
        raise e


@api_view(["GET"])
def tracks_view(request):
    search = request.GET.get("search", "")

    if search == "":
        tracks = get_tracks()
    else:
        tracks = get_tracks()[
            get_tracks()["track_name"].str.contains(
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
