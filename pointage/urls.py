from django.urls import path
from . import views

app_name = 'pointage'

urlpatterns = [
  #  path('', views.dashboard, name='pointage_home'),  # Page principale de pointage
    path('check-in/', views.check_in, name='check_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('check-out/', views.check_out, name='check_out'),
]
