from django.db import models
from accounts.models import ClientList, Profile
from django.contrib.auth.models import User
class Process(models.Model):
	process_id = models.CharField(primary_key=True, max_length=250, unique=True)
	process_name = models.CharField(max_length = 250, null=False, blank=True)
	parent_p_id = models.CharField(max_length=250)
	# user_id = models.CharField(max_length=250)
	client_id= models.ForeignKey(ClientList, on_delete=models.CASCADE, blank=True, null=True)
	user_id= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	# client_id = models.CharField(max_length=250, blank=True)

class Process_List(models.Model):
	process_id = models.OneToOneField(Process, on_delete=models.CASCADE)
	# process_id = models.CharField(primary_key=True,max_length=250,unique=True)
	user_id= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)