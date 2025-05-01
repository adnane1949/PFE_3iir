from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pointage.models import Attendance
from pauses.models import Pause  # Assure-toi que le modèle Pause est importé

@login_required
def dashboard_view(request):
    # Récupérer toutes les présences de l'utilisateur connecté, triées par la date de check-in
    attendances = Attendance.objects.filter(user=request.user).order_by('-check_in_time')

    # Récupérer toutes les pauses de l'utilisateur connecté, triées par la date de début de la pause
    pauses = Pause.objects.filter(user=request.user).order_by('-start_time')

    # Passer les données de présence et de pause à la page du tableau de bord
    return render(request, 'pointage/dashboard.html', {'attendances': attendances, 'pauses': pauses})
