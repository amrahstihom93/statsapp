from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from upload.models import Dataset
from mongoengine import *
# Create your models here.
class Choice(EmbeddedDocument):
    choice_text = StringField(max_length=200)
    votes = IntField(default=0)

class Poll(Document):
    question = StringField(max_length=200)
    pub_date = DateTimeField(help_text='date published')
    choices = ListField(EmbeddedDocumentField(Choice))

		
class mlearn(models.Model):
	mlearn_id = models.CharField(max_length = 250, null=False, blank=True)
	mlearn_name = models.CharField(max_length = 250, null=False, blank=True)
	mlearn_method = models.CharField(max_length = 250, null=False, blank=True)
	mlearn_calculated_value = JSONField(default={})
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	dataset_id = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
	parameters = JSONField(default={})
	test = models.CharField(max_length = 250, null=False, blank=True)