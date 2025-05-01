from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Pause

@login_required
def dashboard_pause_view(request):
    ongoing_pauses = Pause.objects.filter(user=request.user, end_time__isnull=True)
    completed_pauses = Pause.objects.filter(user=request.user).exclude(end_time__isnull=True)

    today = timezone.now().date()

    # Vérifier si une pause de chaque type a été déjà prise aujourd'hui
    has_taken_pause = {
        'Café': Pause.objects.filter(user=request.user, type_of_pause='Café', start_time__date=today).exists(),
        'Déjeuner': Pause.objects.filter(user=request.user, type_of_pause='Déjeuner', start_time__date=today).exists(),
    }

    if request.method == 'POST':
        if 'start_pause' in request.POST:  # Démarrer une pause
            pause_type = request.POST.get('pause_type')

            if has_taken_pause[pause_type]:
                return render(request, 'pauses/dashboard.html', {
                    'ongoing_pauses': ongoing_pauses,
                    'completed_pauses': completed_pauses,
                    'error_message': f"Vous avez déjà pris une pause {pause_type} aujourd'hui."
                })

            # Créer la nouvelle pause
            new_pause = Pause(user=request.user, type_of_pause=pause_type)
            new_pause.save()
            return redirect('pauses:dashboard')

        elif 'end_pause' in request.POST:  # Terminer la pause
            pause_to_end = ongoing_pauses.first()  # Sélectionner la première pause en cours
            if pause_to_end:
                pause_to_end.end_time = timezone.now()
                pause_to_end.save()
            return redirect('pauses:dashboard')

    return render(request, 'pauses/dashboard.html', {
        'ongoing_pauses': ongoing_pauses,
        'completed_pauses': completed_pauses,
        'has_taken_pause': has_taken_pause,
    })
