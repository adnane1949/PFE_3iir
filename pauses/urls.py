from django.urls import path
from . import views

app_name = 'pauses'

urlpatterns = [
    path('', views.dashboard_pause_view, name='dashboard'),  # Affichage du tableau de bord des pauses
   
]
