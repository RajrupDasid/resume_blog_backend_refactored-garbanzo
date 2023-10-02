from django.db import models

# Create your models here.


class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.level}: {self.message}"
