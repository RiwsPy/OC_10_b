from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.index, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('favorite/', views.favorite, name='favorite'),
    path('modify_account/', views.modify_account, name='modify_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('change_email/', views.change_email, name='change_email'),
]
