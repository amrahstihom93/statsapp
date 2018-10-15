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
		training_size  = request.POST['training_size']
		random_state = request.POST['random_state']
		fit_intercept = request.POST['fit_intercept']
		dataset_name = request.POST['dataset']
		idvar = request.POST['idvar']
		dvar = request.POST['dvar']


		fit_intercept = fit_intercept.strip('"')

		print("training_size--->",training_size)
		print("random_state---->",random_state)
		print("fit_intercept---->",fit_intercept)
		print("selected Dataset--->",type(dataset_name))
		print("idvar",idvar)
		susr = str(request.user)
		client = MongoClient()
		db = client.datasetDatadb
		collection = db[request.POST['dataset_id']]
		print(db)
		print(collection)
		dvardat = pd.DataFrame(list(collection.find({dvar:{"$exists":True}})))
		print("dvar######",dvardat)
		idvardat = pd.DataFrame(list(collection.find({idvar:{"$exists":True}})))
		print("idvar######",idvardat)

		dar = [dvar]
		idar = [idvar]

		print("dar######", dar)
		print("idar######", idar)
		training_size = str(training_size)
		training_size = training_size.strip('"')
		print("training_value*********",training_size)
		dataSet = dvardat.iloc[:,[1,0]].values #dataset
		x = dvardat.iloc[:,dvardat.columns.get_loc(dvar)].values #dependent variale
		y = idvardat.iloc[:,idvardat.columns.get_loc(idvar)].values #dependent variale
		x = np.reshape(x, (-1, 1))
		y = np.reshape(y, (-1, 1))

		random_state = str(random_state)
		random_state = random_state.strip('"')
		random_state = int(random_state)

		print("random_state_valuee*********",random_state)
		# Fitting Simple Linear Regression to the dataset
		if random_state == 0:
			from sklearn.cross_validation import train_test_split
			x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = (1-(int(training_size)/100)))
		else:
			from sklearn.cross_validation import train_test_split
			x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = (1-(int(training_size)/100)), random_state = int(random_state))

		# Fitting Simple Linear Regression to the Training set
		from sklearn.linear_model import LinearRegression
		if fit_intercept == "True" or fit_intercept  == "true":
			regressor = LinearRegression(fit_intercept=True)
			print("Regressor--->", regressor)
		else:
			regressor = LinearRegression(fit_intercept=False)
		regressor.fit(x_train, y_train)
		print(dataSet)
		print(x)
		print(y)


	return HttpResponse(request)
