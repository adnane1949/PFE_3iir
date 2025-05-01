from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Pause(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type_of_pause = models.CharField(max_length=100, choices=[('Café', 'Café'), ('Déjeuner', 'Déjeuner')])
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.type_of_pause}"

    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return timezone.now() - self.start_time

    @property
    def get_duration_in_minutes(self):
        if self.end_time:
            duration = self.end_time - self.start_time
            return duration.total_seconds() / 60
        return None
