from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views




urlpatterns = [
  path('', home, name='home'),
  path('login/', login_page, name='login'),
  path('register/', register_page, name = 'register'),
  path('user/', user_page, name = 'user'),
  path('account/', account_settings, name='account'),
  path('products/', products, name='products'),
  path('customers/<str:id>/', customers, name='customers'),
  path('create_order/<str:id>', create_order, name='create_order'),
  path('update_customer/<str:id>', update_customer, name='update_customer'),
  path('update_order/<str:id>', update_order, name='update_order'),
  path('delete_order/<str:id>', delete_order, name='delete'),
  path('logout/', logout_trigger, name="logout"),
  path('reset_password/', auth_views.PasswordResetView.as_view(),name="reset_password"),
  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]