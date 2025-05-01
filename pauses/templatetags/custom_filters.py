from django import template
from datetime import timezone

register = template.Library()

@register.filter
def duration_since(value):
    if not value:
        return "Non défini"
    now = timezone.now()
    duration = now - value
    # Retourne une chaîne formatée en heures et minutes
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{duration.days} jours, {hours} heures, {minutes} minutes"
