from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pymongo
import mongoengine,json, pymongo, pandas, pickle,  numpy as np, pandas as pd,matplotlib.pyplot as plt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from upload.models import Dataset
import joblib
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
from sklearn import linear_model

import statsmodels.api as sm
import os
# Create your views here.



def mlearn(request):
	print('Hiiiiii')
	return render(request, 'mlearn.html')

def calcsregression(request):
	print('We are in calcsregression')
	responseData =''
	result = ''

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

		#Saving the model
		list_pickle_path = 'static/model/linear_model.pkl'
		list_pickle = open(list_pickle_path, 'wb')
		pickle.dump(regressor, list_pickle)
		list_pickle.close()


		# load the model from disk
		loaded_model = pickle.load(open(list_pickle_path, 'rb'))
		print("LOADEDMODEL",loaded_model)
		result_score = loaded_model.score(x_test, y_test)
		#predicting test results
		y_pred = regressor.predict(x_test)
		print("Test score: {0:.2f} %".format(100 * result_score))
		result_score = ("{0:.2f} %".format(100 * result_score))
		print(result_score)
		#print("Prediction--->",y_pred)
		#plotting test results on an image
		xarray = x_test
		xar = []
		x_test = np.array(x_test)
		x_test = x_test.astype(np.float)
		y_test = np.array(y_test)
		y_test = y_test.astype(np.float)
		x_train = np.array(x_train)
		x_train = x_train.astype(np.float)

		from sklearn.metrics import r2_score
		aa = r2_score(y_test, y_pred)
		model =sm.OLS(y_test, x_test).fit()


		rs=model.rsquared
		rs=("{0:0.5}".format(rs))
		rad=model.rsquared_adj
		rad=("{0:0.5}".format(rad))
		smr = str(model.summary())
		stderoe = model.bse
		stderoe = float(stderoe)
		stderoe = ("{0:0.5}".format(100*stderoe))
		pvalue = float(model.pvalues)
		tvalue = float(model.tvalues)
		fvalue = model.fvalue
		fvalue = ("{0:0.5}".format(fvalue))
		pvalue = ("{0:0.5}".format(pvalue))
		tvalue = ("{0:0.5}".format(tvalue))
		print(aa)
		print(model.summary())
		print("rsquared", rs)
		print("rad.", rad)
		print(stderoe)
		print("pvalue",pvalue)
		print("tvalue",tvalue)
		print("fvalue",fvalue)

		responseData = {
           	'summary':result,
        }


		describeDict = {
			"result_score" : "",
			"rsquared" : "",
			"radjective" : "",
			"err_of_estimate" : "",
			"fvalue" : "",
			"pvalue" : "",
			"tvalue" : "",
		}

		describeDict['result_score'] = result_score
		describeDict['rsquared'] = rs
		describeDict['radjective'] = rad
		describeDict['err_of_estimate'] = stderoe
		describeDict['fvalue'] = fvalue
		describeDict['pvalue'] = pvalue
		describeDict['tvalue'] = tvalue
		responseData['summary']=  describeDict
		plt.scatter(x_test, y_test, color = 'red')

		plt.plot(x_train, regressor.predict(x_train), color = 'blue')
		plt.title("Salary vs Experience")
		plt.xlabel(idvar)
		plt.ylabel(dvar)

		plt.savefig("static/test1.png")
		plt.clf()
		print(x_train)
		print("X_TEST--->>>")
		print(x_test)
		print(type(x_test))
		print("Y_TEST--->>>")
		print(y_test)
		print(type(y_test))




		#print(x)
		#print(y)


	return JsonResponse(responseData,safe=False)

def multiregression(request):
	print('we are in multiregression algo')
	responseData =''
	result = ''
	if request.method =='POST':
		training_size  = request.POST['training_size']
		random_state = request.POST['random_state']
		fit_intercept = request.POST['fit_intercept']
		dataset_name = request.POST['dataset']
		dvar = request.POST['dvar']
		idvar = request.POST['idvar']

		print("tsize",training_size)
		print("rstate",random_state)
		print("fint",fit_intercept)
		print("dvar",dvar)
		print("idvar",idvar)


		susr = str(request.user)
		client = MongoClient()
		db = client.datasetDatadb
		collection = db[request.POST['dataset_id']]
		print(db)
		print(collection)
		dvardat = pd.DataFrame(list(collection.find({dvar:{"$exists":True}})))
		dataSet = dvardat.iloc[:,[1,0]].values
		idvardat = pd.DataFrame(list(collection.find({idvar:{"exists":True}})))
		print("dataset",dataSet)
		x = dvardat.iloc[:,dvardat.columns.get_loc(dvar)].values
		x = np.reshape(x,(-1,1))
		print("X",x)

		print("dvar######",dvardat)
		dvar = dvar.split(',')
		idvar = idvar.split(',')

		reg = linear_model.LinearRegression()


		for k in dvar:
			print("dvar",k)
		for i in idvar:
			print("idvar", i)

		m=dvardat[idvar]
		print("m--->",type(m))

		n=dvardat[[k]]
		print("n--->",n)


		reg.fit(dvardat[idvar],dvardat[[k]])
		list_pickle_path='static/model/multi_linear_model.pkl'
		list_pickle = open(list_pickle_path,'wb')
		pickle.dump(reg, list_pickle)
		list_pickle.close()

		loaded_model = pickle.load(open(list_pickle_path, 'rb'))
		print("LOADEDMODEL",loaded_model)

		m = np.array(m)
		n = np.array(n)

		print("coefficient",reg.coef_)
		print("intercept",reg.intercept_)
		pred=reg.predict([[0.21,0.08]])
		print("predicted Score",pred)

		X=sm.add_constant(dvardat[idvar])
		print(X)
		model = sm.OLS(n.astype(float),X.astype(float)).fit()
		predictions = model.predict(X.astype(float))
		print_model = model.summary()
		print(predictions)
		rs= model.rsquared
		rs = ("{0:0.5}".format(rs))
		print ("rsquared",rs)
		rad = model.rsquared_adj
		rad=("{0:0.5}".format(rad))
		print("rsquared_adj",rad)
		stderoe = model.bse
		print("stderoe",stderoe)
		fvalue = model.fvalue
		print("fvalue",type(fvalue))
		print(print_model)
		print()
		responseData ={
			'summary':result,
		}

		describeDict={
		"predicted_score":"",
		"rsquared":"",
		"radjective":"",
		}

		describeDict['predicted_score'] = pred
		describeDict['rsquared'] = rs
		describeDict['radjective'] = rad
		responseData['summary']=  describeDict

		print(describeDict);


	return JsonResponse(responseData,safe=False)

def savemodel(request):
	print('I am in save model function')
	json_data = {}
	data = {}
	if request.method == 'POST':
		filename = request.POST['filename']
		file = 'static/model/linear_model.pkl'
		print(filename)
		print(os.listdir('static/model'))
		print(filename+'.pkl')
		os.rename(file, 'static/model/'+filename+'.pkl')

		msg = 'saved successfully'
		return HttpResponse(msg)
	msg = 'error while saving statistical summary'
	return HttpResponse(msg)

def mlist(request):
	if request.method =='POST':
		filename = request.POST['FileName']

	return HttpResponse(msg)
