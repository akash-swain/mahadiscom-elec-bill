from django.urls import path, include
from .views import BillList

urlpatterns = [
    path('bill/', BillList.as_view() ,name = "detail"),
]
