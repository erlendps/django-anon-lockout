from django.urls import path
from tests.views import index

urlpatterns = [
    path("", index, name="index")
]
