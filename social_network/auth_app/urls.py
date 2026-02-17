from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_reg, name='home'),
    path('register/', views.serv_reg, name='reg_server'),
    path('main/', views.main_menu, name='main_menu'),
    path('login-in-acaunt/', views.login_client, name='log_in_acaunt'),
    path('login/', views.login_serv, name='login_serv'),
    path('logout-in-user/', views.logout, name='logout_user'),
    path('settings/user/chek/', views.serv_verf_password, name='serv_verf_password'),
    path('settings/user/verf/', views.verf_password_settings, name='verf_password'),
    path('update_profile/', views.upd_profil_, name='upd_profil'),
    path('delete_account/', views.del_user, name='delete_user'),
    path('change_password/', views.ch_password, name='ch_passw'),
    path('settings/user/', views.settings, name='settings_user'),
    path('api/get-all/', views.api_users_req, name='api-get-all-users'),
    path('api/get-random-user/', views.api_get_rn_user, name='api-rn-us')
]
