from __future__ import unicode_literals
from apps.accounts.models import ClientList, Profile
from apps.processes.models import Process
from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField


class Dataset(models.Model):
    dataset_name = models.CharField(max_length=255)
    dataset_id = models.CharField(primary_key=True, max_length=255, unique=True)
    document = models.FileField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # Row data stored directly as JSON (replaces MongoDB rowData collection)
    data = JSONField(default=list)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    process_id = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.dataset_name

    class Meta:
        ordering = ['-uploaded_at']


class ColumnMeta(models.Model):
    """
    Stores column name and inferred data type for each dataset column.
    Replaces the MongoDB 'headersData' collection.
    """
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='columns')
    column_name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50, default='string')

    def __str__(self):
        return f"{self.dataset.dataset_name} — {self.column_name} ({self.data_type})"

    class Meta:
        unique_together = ('dataset', 'column_name')


class Dataset_List(models.Model):
    d_id = models.OneToOneField(Dataset, on_delete=models.CASCADE)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    p_id = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)