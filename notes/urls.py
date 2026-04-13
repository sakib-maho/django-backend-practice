from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("notes/", views.note_collection, name="note-collection"),
    path("notes/<int:note_id>/", views.note_detail, name="note-detail"),
]
