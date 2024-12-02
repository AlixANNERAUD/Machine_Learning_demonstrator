from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import plotly.express as px
import numpy
import spotipy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.decorators import api_view

from views import umap_view

configuration = apps.get_app_config("application")

