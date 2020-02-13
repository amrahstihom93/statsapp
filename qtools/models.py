from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from upload.models import Dataset



class fmea(models.Model):
    fmea_name = models.CharField(max_length = 250, null=False, blank=True)
    fmea_sheetid =models.CharField(max_length = 250, null=False, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank =True, null=True)
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)
    parameters = JSONField(default={})
