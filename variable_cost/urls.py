from django.urls import path

from . import views

app_name = "variable_cost"
urlpatterns = [
    path("input", views.InputView.as_view(), name="input"),
    path("list", views.ListView.as_view(), name="list"),
]
