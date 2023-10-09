from django.db import models

# Create your models here.


class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.level}: {self.message}"


class Analytics(models.Model):
    ip = models.CharField(max_length=255, null=True, blank=True, default=None)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    page_url = models.URLField(max_length=255, null=True, blank=True)
    referrer = models.URLField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    device_type = models.CharField(max_length=255, null=True, blank=True)
    screen_resolution = models.CharField(max_length=255, null=True, blank=True)
    operating_system = models.CharField(max_length=255, null=True, blank=True)
    button_clicks = models.IntegerField(default=0)
    form_submissions = models.IntegerField(default=0)
    video_views = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    custom_metric_1 = models.IntegerField(default=0)
    custom_metric_2 = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Ip address logged - {self.ip} || Ip address logged at {self.created}"

    class Meta:
        verbose_name = 'Analytic'
        verbose_name_plural = 'Analytics'
