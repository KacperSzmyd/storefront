from django.urls import include, path

# from django.views.generic import TemplateView
from .views import go_to_api_root

urlpatterns = [path("", go_to_api_root), path("store/", include("store.urls"))]
