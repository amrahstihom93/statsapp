from django.db import models
from django.contrib.auth.models import User
from apps.processes.models import Process
from django.db.models import JSONField


class fmea(models.Model):
    fmea_name = models.CharField(max_length=255, blank=True)
    fmea_sheetid = models.CharField(max_length=255, blank=True)
    # sheet_data replaces MongoDB fmeaDatadb — stores the FMEA rows as JSON
    sheet_data = JSONField(default=list)
    # Legacy field kept for backward compatibility (now unused)
    parameters = models.TextField(blank=True, default='')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.fmea_name

    class Meta:
        verbose_name = 'FMEA Sheet'
        verbose_name_plural = 'FMEA Sheets'
