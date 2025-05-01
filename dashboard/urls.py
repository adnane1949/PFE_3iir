from django.urls import path
from . import views
from django.http import HttpResponse

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # Tableau de bord
    path('', lambda request: HttpResponse("Bienvenue sur la page d'accueil !")),
]
