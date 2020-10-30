from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from upload.models import Dataset

# database model class for visualziation module
class visualization(models.Model):
	visualization_id = models.CharField(max_length = 250, null=False, blank=True)
	visualization_name = models.CharField(max_length = 250, null=False, blank=True)
	type = models.CharField(max_length = 250, null=False, blank=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
	parameters = JSONField(default={})	