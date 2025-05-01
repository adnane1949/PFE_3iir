from django.urls import path
from . import views

app_name = 'utilisateurs'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # fonctionne après avoir ajouté la vue
    path('register/', views.signup_view, name='register'),  # si tu as une vue register
]
