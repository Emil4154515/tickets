from django.urls import path
from . import views

urlpatterns = [
    # Authorization
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.index, name='index'),
]
