from django.db import models


class Log(models.Model):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    LEVEL_CHOICES = ((DEBUG, DEBUG), (INFO, INFO), (WARNING, WARNING), (ERROR, ERROR), (CRITICAL, CRITICAL))

    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(choices=LEVEL_CHOICES, blank=False, max_length=50)
    path = models.CharField(blank=False, max_length=200)
    message = models.TextField(blank=False)

    class Meta:
        db_table = "log"
