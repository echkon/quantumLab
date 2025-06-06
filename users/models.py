from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class WorkSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        start_time_local = timezone.localtime(self.start_time)
        end_time_local = timezone.localtime(self.end_time) if self.end_time else None
        return f"Working Record for {self.user.username}, Started at {start_time_local}, Stopped at {end_time_local}"

    @property
    def duration(self):
        if self.end_time:
            duration = self.end_time - self.start_time
            # Convert to local time for the duration calculation if necessary
            return duration
        return None