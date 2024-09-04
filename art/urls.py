from django.urls import path
from .views import ArtDetailView, CreateArtView, save_art
app_name = 'art'
urlpatterns = [
    path("art_deltail/<int:art_id>/", ArtDetailView.as_view(), name = "art_deltail"),
    path("create_art/", CreateArtView.as_view(), name = "create_art"),
    path("save_art/<int:user_id>/", save_art, name = "save_art"),
]