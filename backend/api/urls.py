from django.urls import path
from .views import InputDataListCreate , SessionDataView

urlpatterns = [
   path('data/', InputDataListCreate.as_view(), name='data-list-create'),
   path("session-data/", SessionDataView.as_view(), name="session-data"),
]

