from django.urls import path

from . import views

app_name = "verdvaktin"
urlpatterns = [
    path("", views.IndexView.as_view()),
    path("save/<slug:cpu_id>", views.save, name="save"),
]
