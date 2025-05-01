from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance
from django.contrib.auth.decorators import login_required
from math import radians, sin, cos, sqrt, atan2

# Coordonnées du point central (ex : Casablanca)
LAT_CENTRAL = 33.5894
LON_CENTRAL = -7.6110
RADIUS_KM = 0.5  # Rayon en kilomètres

# Fonction pour calculer la distance entre deux coordonnées géographiques
def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius = 6371.0  # Rayon de la Terre en kilomètres
    return radius * c

@login_required
def check_in(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Vérifie que les coordonnées sont bien présentes
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)

            # Calcul de la distance
            distance = calculate_distance(LAT_CENTRAL, LON_CENTRAL, latitude, longitude)

            # Si dans le rayon autorisé, enregistrer la présence
            if distance <= RADIUS_KM:
                attendance = Attendance(user=request.user, check_in_time=timezone.now(), latitude=latitude, longitude=longitude)
                attendance.save()
                return redirect('pointage:dashboard')
            else:
                return render(request, 'pointage/check_in.html', {'error': "Vous devez être dans un rayon de 0.5 km."})
        else:
            return render(request, 'pointage/check_in.html', {'error': "Coordonnées invalides."})

    return render(request, 'pointage/check_in.html')

@login_required
def check_out(request):
    if request.method == 'POST':
        # Trouver l'enregistrement de pointage sans check_out_time
        attendance = Attendance.objects.filter(user=request.user, check_out_time__isnull=True).last()

        if attendance:
            # Si un pointage actif est trouvé, on met à jour l'heure de sortie
            attendance.check_out_time = timezone.now()
            attendance.save()
            return redirect('pointage:dashboard')
        else:
            return render(request, 'pointage/check_out.html', {'error': "Aucun pointage actif trouvé."})

    return render(request, 'pointage/check_out.html')

@login_required
def dashboard(request):
    attendances = Attendance.objects.filter(user=request.user).order_by('-check_in_time')
    active_attendance = attendances.filter(check_out_time__isnull=True).first()
    return render(request, 'pointage/dashboard.html', {'attendances': attendances, 'active_attendance': active_attendance})
