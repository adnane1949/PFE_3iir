from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from pointage.models import Attendance
from django.utils import timezone

def login_view(request):
    next_page = request.GET.get('next', 'dashboard:dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Pointage automatique lors de la connexion
            Attendance.objects.create(
                user=user, 
                check_in_time=timezone.now()
            )
            
            return redirect(next_page)
    else:
        form = AuthenticationForm()
    return render(request, 'utilisateurs/login.html', {'form': form})


# Formulaire d'inscription utilisateur

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('utilisateurs:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'utilisateurs/signup.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return redirect('utilisateurs:login')