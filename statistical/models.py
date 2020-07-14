from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from upload.models import Dataset

class statistical(models.Model):
	statistical_id = models.CharField(max_length = 250, null=False, blank=True)
	statistical_name = models.CharField(max_length = 250, null=False, blank=True)
	statistical_method = models.CharField(max_length = 250, null=False, blank=True)
	statistical_calculated_value = JSONField(default={})
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
	parameters = JSONField(default={})
	test = models.CharField(max_length = 250, null=False, blank=True)


class analytical(models.Model):
	analytical_id = models.CharField(max_length = 250, null=False, blank=True)
	analytical_name = models.CharField(max_length = 250, null=False, blank=True)
	analytical_method = models.CharField(max_length = 250, null=False, blank=True)
	analytical_calculated_value = JSONField(default={})
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
	parameters = JSONField(default={})
	test = models.CharField(max_length = 250, null=False, blank=True)

class hypothetical(models.Model):
	hypothetical_id = models.CharField(max_length = 250, null=False, blank=True)
	hypothetical_name = models.CharField(max_length = 250, null=False, blank=True)
	hypothetical_method = models.CharField(max_length = 250, null=False, blank=True)
	hypothetical_calculated_value = JSONField(default={})
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
	parameters = JSONField(default={})
	test = models.CharField(max_length = 250, null=False, blank=True)
