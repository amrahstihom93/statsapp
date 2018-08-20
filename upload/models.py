from __future__ import unicode_literals
from accounts.models import ClientList, Profile
from process.models import Process
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models
		
class Dataset(models.Model):
	dataset_name = models.CharField(max_length=255)
	dataset_id = models.CharField(primary_key=True, max_length=255, unique=True)
	document = models.FileField()
	uploaded_at = models.DateTimeField(auto_now_add=True)
	data = JSONField(default={})
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	process_id = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)
	
	def __str__(self):
		return self.dataset_name


class Dataset_List(models.Model):
	d_id = models.OneToOneField(Dataset, on_delete=models.CASCADE)
	u_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	p_id = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True, null=True)