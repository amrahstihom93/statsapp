from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pymongo
import mongoengine,json, pymongo, pandas, pickle,  numpy as np, pandas as pd,matplotlib.pyplot as plt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from upload.models import Dataset

from django.contrib.auth.models import User
import json, datetime
import pandas as pd
from pymongo import MongoClient
from io import StringIO
import statistics
from statistics import mode
import matplotlib.pyplot as plt
import scipy.stats.stats as stats
from scipy.stats import kurtosis
from scipy import stats

# Create your views here.



def mlearn(request):
	print('Hiiiiii')
	return render(request, 'mlearn.html')

def calcsregression(request):
	print('We are in calcsregression')
	if request.method == 'POST':
		fieldsArr = []
		print(fieldsArr)
		print("in calc POSTMEHTOD")
		print(request.POST['training_size'])
		print(request.POST['random_state'])
		print(request.POST['fit_intercept'])

		print("Dataset ID =", request.POST['dataset_id'])

		susr = str(request.user)
		client = MongoClient()
		db = client.datasetDatadb
		collection = db[request.POST['dataset_id']]
		datav = collection.find( { } )
		pd.set_option('display.max_columns', None)
		print (db)
	return HttpResponse(request)
