from django.urls import path, include
from .views import BillList, activate, signup, listdelete, listdeletewater
from django.contrib.auth import views as auth_views

# app_name = "de"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='billapp/login.html') ,name = "main"),
    path('logout/', auth_views.LogoutView.as_view(), name = "logout"),
    path('', BillList.as_view() ,name = "detail"),
    path('delete/<str:consumerno>', listdelete ,name = "delete"),
    path('delete_water/<str:consumerno>', listdeletewater ,name = "delete-water"),
    # path("thanks/", ThanksPage.as_view(), name="thanks"),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>', activate,name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),  name='password_reset'),
    # path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_reset_done.html' ),  name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]
