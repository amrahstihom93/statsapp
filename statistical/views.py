import pymongo
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from upload.models import Dataset
from .models import statistical
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

def saveAnalytics(request):
	print('I am in save function')
	vForm = analytical()
	json_data = {}
	data = {}
	if request.method == 'POST':
	    vForm.analytical_name = request.POST['analytical_name']
	    dataset_obj = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
	    user_obj = User.objects.get(pk=request.user.id)
	    vForm.user_id = user_obj
	    vForm.dataset_id = dataset_obj
	    vForm.analytical_id = 'sid' + request.POST['analytical_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	    vForm.analytical_method = request.POST['selectedmethod'] 
	    print('hi from save to all')
	    vForm.analytical_calculated_value = request.POST['analytical_calculated_value']
	#    data = request.POST['fieldData']
	#    json_data = json.loads(data)
	    vForm.parameters = request.POST['fieldData']
	    vForm.save()
	    msg = 'saved successfully'
	    return HttpResponse(msg)
	msg = 'error while saving analytical summary'
	return HttpResponse(msg)



def saveStatistics(request):
	print('I am in save function')
	vForm = statistical()
	json_data = {}
	data = {}
	if request.method == 'POST':
	    vForm.statistical_name = request.POST['statistical_name']
	    dataset_obj = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
	    user_obj = User.objects.get(pk=request.user.id)
	    vForm.user_id = user_obj
	    vForm.dataset_id = dataset_obj
	    vForm.statistical_id = 'sid' + request.POST['statistical_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	    vForm.statistical_method = request.POST['selectedmethod'] 
	    print('hi from save to all')
	    vForm.statistical_calculated_value = request.POST['statistical_calculated_value']
	#    data = request.POST['fieldData']
	#    json_data = json.loads(data)
	    vForm.parameters = request.POST['fieldData']
	    vForm.save()
	    msg = 'saved successfully'
	    return HttpResponse(msg)
	msg = 'error while saving statistical summary'
	return HttpResponse(msg)
	
	


def calculateAnalytics(request):
	print('Hiiiiiiiiii')

	
	if request.method == 'POST':
		result = 0
		res = 0
		print("In Post Method")
		fieldsArr = []
		print(fieldsArr)
		selectedgroup = request.POST['selectedgroup']
		selecteddatacol = request.POST['selecteddatacol']		
		print("Group = ",request.POST['selectedgroup'])
		print("Data = ", request.POST['selecteddatacol'])
		print("Test Method =", request.POST['selectedmethod'])
		print("Dataset ID =", request.POST['dataset_id'])
		
		susr = str(request.user)
		client = MongoClient()
		db = client.datasetDatadb
		collection = db[request.POST['dataset_id']]
		data = collection.find( { } )
		#print(str(data))
	#dataFromMongo = collection.find({y: {"$exists": True}})
        #for doc in dataFromMongo:
            #default_items.append(doc[y])
		t = collection.find({selectedgroup: {"$exists": True}})
		datag = pd.DataFrame(list(collection.find({selectedgroup:{"$exists":True}})))
		datac = pd.DataFrame(list(collection.find({selecteddatacol:{"$exists":True}})))
		#print('Jasnoor',data)
		#print("########", type(data))
		og = list(datag.loc[:,selectedgroup])
		oc = list(datac.loc[:,selecteddatacol])
		
		#print(og)
		#print(datag)
		#print('Group',type(og))
		xx = pd.DataFrame(oc, og)
		#print('xx datatype',type(xx))
		print(xx)
		
		csv = pd.DataFrame.to_csv(xx)
		print(csv)
		sd = pd.read_csv(StringIO(csv))
		print(sd)
		k = len(pd.unique(sd.selectedgroup))
		print(ls)
		#sc = collection.find({selectedgroup: {"$exists": True}})
		#print(ogl)
		'''for doc in g and doc in c:
			print("Printing DOC")
			print(doc in g and soc in c)'''
		#print(list(g,c))
		#data_c = pd.DataFrame(list(data))
		#data_g = pd.DataFrame(list(collection.find({selectedgroup: {"$exists": True}})))
		#print(data_c)
		#print(data_g)
		#print("########", type(data_g))
		#print(data_c)
		#print("########", type(data_c))
		#og = list(data_c.loc[:,selectedgroup])
		#oc = list(data_c.loc[:,selecteddatacol])
		#print('####selectedgroup', dg)
		#print('Project',type(sc))
		#xg = pd.DataFrame(sc)
		#xc = pd.DataFrame(oc)
		#print(xg)
		#csv_g = pd.DataFrame.to_csv(xg)
		#sd_g = pd.read_csv(StringIO(csv_g))
		#print('type of data1',type(sd_g))
		#ls_g = sd_g.describe()
		
		#csv_c = pd.DataFrame.to_csv(xc)
		#sd_c = pd.read_csv(StringIO(csv_c))
		#print('type of data2',type(sd_c))
		
		#ls_c = sd_c.describe()
		# print('location',ls.loc[1])
		
		#print('The final result group',type(ls_g))
		#print('The final result datacol',type(ls_c))
	
		responseData = {
           	'summary':result,
			'fieldData':og,
			'selectedgroup': request.POST['selectedgroup']
        }
		#l = pd.DataFrame.to_csv(ls)
		#lg = pd.DataFrame.to_json(ls_g)
		#lc = pd.DataFrame.to_json(ls_c)
		#print("###only median",med)
		#print(ls.loc["mean","0"])
		#responseData['summary'] = 100
		describeDict = {
			"count" : "",
			"mean" : "",
			"std" : "",
			"median": "",
			"skewness": "",
			"kurtosis":"",
			"min" :"",
			"25" : "",
			"50" : "",
			"75" : "",
			"max" : ""
		}
		print(request.POST['selectedgroup'])
		if request.POST['selectedmethod'] == 'anova':
			#k=len(pd.unique(data))
			#grps = pd.unique(data_g.values)
			#d_data= {grp:}
			responseData['summary']=  describeDict
			
		
		return JsonResponse(responseData)
	
	
	
def calculateStatistics(request):
	print('Hiiiiiiiiii')

	
	if request.method == 'POST':
		result = 0
		res = 0
		print("In Post Method")
		fieldsArr = []
		print(fieldsArr)
		selectedfield = request.POST['selectedfield'] 
		print(request.POST['selectedfield'])
		print(request.POST['selectedmethod'])
		print(request.POST['dataset_id'])
	# dataset_id = request.POST['dName']
	# print(dataset_id)
		
		susr = str(request.user)
		client = MongoClient()
		db = client.datasetDatadb
		collection = db[request.POST['dataset_id']]
		#data = collection.find( { } )
		#print(str(data))
	#dataFromMongo = collection.find({y: {"$exists": True}})
    #    for doc in dataFromMongo:
    #        default_items.append(doc[y])
		t = collection.find({selectedfield: {"$exists": True}})
		for doc in t:
			print(doc)
		print(list(t))
		data = pd.DataFrame(list(collection.find({selectedfield: {"$exists": True}})))
		print('Jasnoor',data)
		print("########", type(data))
		oo = list(data.loc[:,selectedfield])
		print('####selectedfield', oo)
		print('Porject',type(oo))
		xx = pd.DataFrame(oo)
		print('xx datatype',type(xx))
		#for doc in data:
		#	print(doc)
            #default_items.append(doc[y])
		#print(data)
		#print(type(data))
		# s = data.loc['selectedfield']
		# print(s)
		csv = pd.DataFrame.to_csv(xx)
		sd = pd.read_csv(StringIO(csv))
		print('type of data1',type(sd))
		ls = sd.describe()
		# print('location',ls.loc[1])
		print('The final result',type(ls))
	#	plot = plt.hist(ls)
		# plt.savefig('abs.png')
	#	plt.show()
		# plt.close()
		# if request.POST['selectedmethod'] == 'median':
		# 	med = sd.median()
		# 	med1 = med.to_frame()
		# 	#print('####### med1', med1.loc["0",:])
		# 	print('#### new med1', med1.iloc[1][0])
		# 	finalMedian = med1.iloc[1][0]
		# 	#lmed1 = med1.to_json()
		# 	print('calculated value of median',med)
		# 	print('Median Type',type(med))
		# 	print('Median value',med1)
		# 	print('type of data frame',type(med1))
		if request.POST['selectedmethod'] == 'mode':
			mod = sd.mode()
			print('Mode Value', mod)
			mod1 = mod.to_frame()
			# print('##### new mode',mod1)
			lmod1 = mod1.to_json()

		# mod = sd.mode(
		# print(mod)
		# print(ls)
		# print(med)
		# print('Meidan',type(med))
		responseData = {
           	'summary':result,
			'fieldData':oo,
			'selectedfield': request.POST['selectedfield']
        }
		#l = pd.DataFrame.to_csv(ls)
		l = pd.DataFrame.to_json(ls)
		#print("###only median",med)
		#print(ls.loc["mean","0"])
		#responseData['summary'] = 100
		describeDict = {
			"count" : "",
			"mean" : "",
			"std" : "",
			"median": "",
			"skewness": "",
			"kurtosis":"",
			"min" :"",
			"25" : "",
			"50" : "",
			"75" : "",
			"max" : ""
		}
		print(request.POST['selectedfield'])
		if request.POST['selectedmethod'] == 'describe':
			med = sd.median()
			med1 = med.to_frame()
			ske = sd.skew()
			ske1 = ske.to_frame()
			kurt = sd.kurtosis()
			kurt1 = kurt.to_frame()
			describeDict['count'] = ls.loc["count","0"]
			describeDict['mean'] = ls.loc["mean","0"]
			describeDict['std'] = ls.loc["std","0"]
			describeDict['min'] = ls.loc["min","0"]
			describeDict['median'] = med1.iloc[1][0]
			describeDict['skewness'] = ske1.iloc[1][0]
			describeDict['kurtosis'] = kurt1.iloc[1][0]
			describeDict['25'] = ls.loc["25%","0"]
			describeDict['50'] = ls.loc["50%","0"]
			describeDict['75'] = ls.loc["75%","0"]
			describeDict['max'] = ls.loc["max","0"]
			responseData['summary']=  describeDict
		if request.POST['selectedmethod'] == 'mode':
			responseData['summary'] = lmod1
		# print('response', responseData)
		# print('##EEE',ls.loc[:,"0"])
		# print('ls json', ls.loc[:,"0"].to_json())
		# print(type(ls))
		# #print(type(data))
		# responseData = {
  #          	'summary':result,
		# 	'fieldData':csv,
		# 	'selectedfield': request.POST['selectedfield']
  #       }
		return JsonResponse(responseData)


		
def getAnalyticalList(request):
    usr = str(request.user)
    listObj = []
    try:
        print('in analyticalList')
        analyticalList = analytical.objects.filter(user_id=request.user.id).values()
        if len(analyticalList) > 0:
            for i in range(len(analyticalList)):
                listObj.append(analyticalList[i])
                print('xxx', analyticalList[i])
        return JsonResponse(listObj, safe=False)
    except:
        msg = 'error while getting datasets'
    return HttpResponse(msg)		


		
def getStatisticalList(request):
    usr = str(request.user)
    listObj = []
    try:
        print('in statisticalList')
        statisticalList = statistical.objects.filter(user_id=request.user.id).values()
        if len(statisticalList) > 0:
            for i in range(len(statisticalList)):
                listObj.append(statisticalList[i])
                print('xxx', statisticalList[i])
        return JsonResponse(listObj, safe=False)
    except:
        msg = 'error while getting datasets'
    return HttpResponse(msg)

	

def delAnalytical(request, id):
	print('In Delete Method')
	res = ''
	try:
	    analyticalToDelete = analytical.objects.get(pk=id)
	    analyticalToDelete.delete()
	    res = 'delete successful'
	except:
	    res = 'delete unsuccessful'
	return HttpResponse(res)

def delStatistical(request, id):
	print('In Delete Method')
	res = ''
	try:
	    statisticalToDelete = statistical.objects.get(pk=id)
	    statisticalToDelete.delete()
	    res = 'delete successful'
	except:
	    res = 'delete unsuccessful'
	return HttpResponse(res)