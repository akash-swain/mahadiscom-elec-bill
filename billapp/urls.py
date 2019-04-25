from django.urls import path, include
from .views import BillList

urlpatterns = [
    path('', BillList.as_view() ,name = "detail"),
]
