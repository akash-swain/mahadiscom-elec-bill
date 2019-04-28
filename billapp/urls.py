from django.urls import path, include
from .views import BillList, ThanksPage
from django.contrib.auth import views as auth_views

# app_name = "de"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='billapp/login.html') ,name = "main"),
    path('logout/', auth_views.LogoutView.as_view(), name = "logout"),
    path('', BillList.as_view() ,name = "detail"),
    path("thanks/", ThanksPage.as_view(), name="thanks"),
    # path('logout/', BillList.as_view() ,name = "logout"),
]
