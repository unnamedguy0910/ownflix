from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('create/', views.create_room, name='create_room'),
    path('join-room/', views.join_room, name='join_room'),
    path('room/<slug:room_slug>/', views.room_view, name='room'),
]
