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
from json import JSONEncoder
from .models import mlearn
import statsmodels.api as sm
import os
# Create your views here.

regressor = 1
list_pickle = 1

#regression model calculation
def calcsregression(request):
	print('We are in calcsregression')
	global describeDict
	global responseData
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
		print(type(x))
		print("X",x)
		print(type(y))
		print("Y",y)

		x = np.reshape(x, (-1, 1))
		print("reshaped",x)
		y = np.reshape(y, (-1, 1))
		print("reshaped",y)
		random_state = str(random_state)
		random_state = random_state.strip('"')
		random_state = int(random_state)

		print("random_state_valuee*********",random_state)
		# Fitting Simple Linear Regression to the dataset
		if random_state == 0:
			from sklearn.model_selection import train_test_split
			x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = (1-(int(training_size)/100)))
		else:
			from sklearn.model_selection import train_test_split
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
		pvalue = ("{0:0.3f}".format(pvalue))
		tvalue = ("{0:0.5}".format(tvalue))
		print(aa)
		print(model.summary())
		print("rsquared", rs)
		print("rad.", rad)
		print(stderoe)
		print("pvalue",pvalue)
		print("tvalue",tvalue)
		print("fvalue",fvalue)

		xtrain_pred=regressor.predict(x_train)
		print(x_train)
		print(xtrain_pred)
		print(list(x_train))
		print(type(xtrain_pred))
		x_train_conv=list(xtrain_pred)
		x_train2 = list(x_train)
		print(x_train_conv)

		class NumpyArrayEncoder(JSONEncoder):
			def default(self, obj):
				if isinstance(obj, np.ndarray):
					return obj.tolist()
				return JSONEncoder.default(self, obj)
		# Serialization
		numpyxtrain = {"xtrain_array": xtrain_pred}
		numpyData = {"conv_pred_array": x_train2}
		encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)  # use dump() to write array into file
		encodedpredData = json.dumps(numpyxtrain, cls=NumpyArrayEncoder)  # use dump() to write array into file
		print("Printing JSON serialized NumPy array")
		print(encodedNumpyData)
		print(encodedpredData)

		numpyxtest = {"xtest_array" : x_test}
		numpyytest = {"ytest_array" : y_test}
		x_test_dat=json.dumps(numpyxtest, cls=NumpyArrayEncoder)
		y_test_dat=json.dumps(numpyytest, cls=NumpyArrayEncoder)

		print("Printing JSON SERIALIZED XTEST AND YTEST")
		print(x_test_dat)
		print(y_test_dat)


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
			"xtest" : "",
			"ytest" : "",
			"xtrain" : "",
			"xtrain_pred" : "",
		}

		describeDict['result_score'] = result_score
		describeDict['rsquared'] = rs
		describeDict['radjective'] = rad
		describeDict['err_of_estimate'] = stderoe
		describeDict['fvalue'] = fvalue
		describeDict['pvalue'] = pvalue
		describeDict['tvalue'] = tvalue
		describeDict['xtrain'] = encodedNumpyData
		describeDict['xtrain_pred'] = encodedpredData
		describeDict['xtest'] = x_test_dat
		describeDict['ytest'] = y_test_dat
		responseData['summary']=  describeDict
		# plt.scatter(x_test, y_test, color = 'red')
		#
		# plt.plot(x_train, regressor.predict(x_train), color = 'blue')
		plt.title("Salary vs Experience")
		plt.xlabel(idvar)
		plt.ylabel(dvar)
		#
		# plt.savefig("static/test1.png")
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

# formatting and saving modal values in database
def saveMLmodel(request):
	print(describeDict)
	print('I am in save model function')
	list_pickle_path = 'static/model/linear_model.pkl'
	list_pickle = open(list_pickle_path, 'wb')
	pickle.dump(regressor, list_pickle)
	list_pickle.close()


	# load the model from disk
	loaded_model = pickle.load(open(list_pickle_path, 'rb'))
	pickled_model = pickle.dumps(loaded_model)
	client =MongoClient()
	db = client.mlearnDatadb
	print(client.list_database_names())
	print(db.list_collection_names())
	collection_name = "mlearnData"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	col = db[collection_name]
	if request.method == 'POST':
		vForm = mlearn()
		json_data = {}

		data = {}
		data['result_score'] = describeDict.get('result_score')
		data['rsquared'] = describeDict.get('rsquared')
		data['radjective'] = describeDict.get('radjective')
		data['err_of_estimate'] = describeDict.get('err_of_estimate')
		data['fvalue'] = describeDict.get('fvalue')
		data['pvalue'] = describeDict.get('pvalue')
		data['tvalue'] = describeDict.get('tvalue')
		datad =  json.dumps(data, indent = 4)
		print(datad)
		model_name  = request.POST['model_name']
		vForm.mlearn_name= request.POST['model_name']
		user_obj = User.objects.get(pk=request.user.id)
		vForm.user_id=user_obj
		print("postgorm",vForm)

		colId = col.insert_one({"model":pickled_model, "model_name" : model_name, 'calculated_values' : datad })
		msg = 'saved successfully'
		print(colId.inserted_id)
		vForm.mlearn_id = collection_name
		vForm.parameters = datad
		vForm.save()
		filename = request.POST['model_name']
		file = 'static/model/linear_model.pkl'
		print(filename)
		print(os.listdir('static/model'))
		print(filename+'.pkl')
		os.rename(file, 'static/model/'+filename+'.pkl')
		msg = 'saved successfully'
		return HttpResponse(msg)

	msg = 'error while saving mlearn model'
	return HttpResponse(msg)
def savemodel(request):

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

# multiple regression modal (inclomplete still formatting needs to be done)
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
		dvardat = pd.DataFrame(list(collection.find({dvar:{"$exists":True}})))
		idvararr = []
		idvararr = [idvar]
		print(idvararr)
		# dataSet = dvardat.iloc[:,[1,0]].values
		dataSet = dvardat.iloc[:,:-1].values
		dataSett = dvardat.iloc[:,[1,0]].values
		print("DATASET&&&",dataSet)
		print("DATASETT&&&",dataSett)
		###idvardat = pd.DataFrame(list(collection.find({idvar[0]:{"exists":True}})))
		###print("idvardat")
		###print(idvardat)
		xt = dvardat[dvar]
		xt=xt.to_frame()
		print("XT09090909090",type(xt))
		print("XT09090909090",xt)

		x = dvardat.iloc[:,dvardat.columns.get_loc(dvar)].values
		#print("X909000009009",x)
		dvar = dvar.split()
		print("ndvar",dvar)
		idvar = idvar.split(',')
		print("nidvar",idvar)
		yt = dvardat[idvar]
		print("YT900909090909",type(yt))
		xt = np.reshape(xt,(-1,1))
		print("XT900909090909",xt)
		#print("X",x)


		reg = linear_model.LinearRegression()
		random_state = str(random_state)
		random_state = random_state.strip('"')
		random_state = int(random_state)
		'''if random_state == 0:
			from sklearn.cross_validation import train_test_split
			x_train, x_test, y_train, y_test = train_test_split(xt, yt, test_size = (1-(int(training_size)/100)))
		else:
			from sklearn.cross_validation import train_test_split
			x_train, x_test, y_train, y_test = train_test_split(xt, yt, test_size = (1-(int(training_size)/100)), random_state = int(random_state))
		'''
		for k in dvar:
			print("dvar",k)
		for i in idvar:
			print("idvar", i)

		m = dvardat[idvar]
		m = m.values

		n = dvardat[[k]]
		n = n.values

		print(type(yt))
		print("YT VALUES",yt.values)
		print(type(xt))
		print("XT VALUES", xt.values)

		#reg.fit(dvardat[idvar],dvardat[[k]])
		reg.fit(yt,xt)
		list_pickle_path='static/model/multi_linear_model.pkl'
		list_pickle = open(list_pickle_path,'wb')
		pickle.dump(reg, list_pickle)
		list_pickle.close()

		loaded_model = pickle.load(open(list_pickle_path, 'rb'))
		print("LOADEDMODEL",loaded_model)

		m = np.array(m)
		n = np.array(n)
		score = loaded_model.score(yt,xt)
		print("score",score)
		print("coefficient",type(reg.coef_))
		coeff = reg.coef_
		print("intercept",reg.intercept_)
		#pred=reg.predict([[0.21,0.08]])
		#print("predicted Score",pred)

		X=sm.add_constant(dvardat[idvar])
		print(X)
		xt = np.array(xt)
		xt = xt.astype(np.float)
		print("TYPE AFTER CASTING",type(xt))
		yt = np.array(yt)
		yt = yt.astype(np.float)
		print("TYPE AFTER CASTING",type(yt))
		model1 = sm.OLS(xt,yt).fit()
		print(model1.summary())
		model = sm.OLS(n.astype(float),X.astype(float)).fit()
		predictions = model.predict(X.astype(float))
		print_model = model.summary()
		rs= model.rsquared
		rs = ("{0:0.5}".format(rs))
		print ("rsquared",rs)
		rad = model.rsquared_adj
		rad=("{0:0.5}".format(rad))
		print("rsquared_adj",rad)
		stderoe = model.bse
		print("stderoe",stderoe)
		fvalue = model.fvalue
		pvalue = model.pvalues
		pvalue = (model.pvalues).to_json()
		print("pvaltype",pvalue)
		print("fvalue",fvalue)
		print(print_model)
		coeff = np.array(coeff).tolist()

		print("coefficients",coeff)
		responseData ={
			'summary':result,
		}

		describeDict={
		"rsquared":"",
		"radjective":"",
		"coefficient":"",
		"fvalue":"",
		"pvalue":"",
		}
		describeDict['coefficients'] = coeff
		describeDict['rsquared'] = rs
		describeDict['radjective'] = rad
		describeDict['fvalue'] = fvalue
		describeDict['pvalue'] = pvalue
		responseData['summary']=  describeDict

		print(describeDict);


	return JsonResponse(responseData,safe=False)

"""def logisticregression(request):
	print('we are in logisticregression')
	responseData = ''
	result = ''
	if request.method == 'POST':
		training_size  = request.POST['training_size']
		random_state = request.POST['random_state']
		fit_intercept = request.POST['fit_intercept']
"""
def mldat(request):
	msg = "inside mldat"
	client = MongoClient()
	print(client.list_database_names())
	db = client.mlearnDatadb
	collection_names = db.list_collection_names()
	print(collection_names)

	return HttpResponse(msg)

def mlist(request):
	msg = "insideListmlearn"
	client = MongoClient()
	print(client.list_database_names())
	collection_name = "mlearn"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	db = client.mlearnDatadb
	print("collections in your dataset",db.list_collection_names())
	collection_names = db.list_collection_names()
	print(type(collection_names))
	print(*collection_names, sep='\n')
	try:
		listObj=[]
		usr=str(request.user)
		print('list0')
		# list = Process.objects.filter(user_id=usr.id).values()\
		mlearnList= mlearn.objects.filter(user_id=request.user.id).values()
		# fmeaObj=fmea.objects.filter(fmea_name).values()
		print("mlearnList",mlearnList)
        # print("fmeaObj",fmeaObj)
        # list = Process.objects.get(user_id=request.user.id).values()
        # print('list',list)
		if len(mlearnList) > 0:
			for i in range(len(mlearnList)):
				listObj.append(mlearnList[i])
				print("%%%%",listObj[i])
            # res = [ sub['fmea_name'] for sub in listObj]
            # print(res)
		return JsonResponse(listObj,safe=False)
	except:
		msg = 'error while getting process list'
		print(msg)

	return HttpResponse(msg)
