import pymongo
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from upload.models import Dataset
from .models import statistical
from .models import analytical
from .models import hypothetical
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
	    print("$$$$$", type(vForm.analytical_calculated_value))
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
		#data = request.POST['fieldData']
		#json_data = json.loads(data)
		vForm.parameters = request.POST['fieldData']
		vForm.save()
		msg = 'saved successfully'
		return HttpResponse(msg)
	msg = 'error while saving statistical summary'
	return HttpResponse(msg)

#saveHypoyhesis
def saveHypothesis(request):

	client = MongoClient()

	db = client.hypoDatadb
	print(client.list_database_names())
	print(db.list_collection_names())

	collection_name = "hypoData"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
	col = db[collection_name]

	print('I am in Save Function of Hypothesis testing')
	vForm = hypothetical()
	json_data = {}
	data = {}
	if request.method =='POST':
		vForm.hypothetical_name = request.POST['hypothetical_name']
		user_obj = User.objects.get(pk=request.user.id)
		dataset_obj = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
		vForm.hypothetical_method = request.POST['hypothetical_method']
		vForm.dataset_id = dataset_obj
		vForm.hypothetical_id = 'hid' + request.POST['hypothetical_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
		vForm.user_id=user_obj
		vForm.hypothetical_calculated_value = request.POST['hypothetical_calculated_value']
		datdoc = json.loads(vForm.hypothetical_calculated_value)
		print("summary", vForm.hypothetical_calculated_value)
		print("summary datadoc",datdoc)
		my_data_file = open('data.txt', 'a')
		with open('data.txt', 'a') as f:
			data = [vForm.hypothetical_method, vForm.hypothetical_calculated_value]
			f.writelines("%s\n" % line for line in data)

		colId=col.insert_one(datdoc)
		print(colId.inserted_id)
		vForm.test = colId.inserted_id
		print(vForm.test)
		vForm.save()
		msg= 'saved successfully'
		return HttpResponse(msg)
	msg = 'error while saving hypothetical summary'
	return HttpResponse(msg)
#calculateHypothesis
def calculateHypothesis(request):
	print('into Calculate Hypothesis')
	if request.method == 'POST':
		print("in POST method")
		result=0

		selecteddatacol = request.POST['selecteddatacol']
		selectedtest = request.POST['selectedtest']

		print("Test  =", request.POST['selectedtest'])
		print("Dataset ID =", request.POST['dataset_id'])
		print("Data = ", request.POST['selecteddatacol'])
		#connecting to database and fetching data column
		susr = str(request.user)
		client = MongoClient()
		db = client.datasetDatadb
		collection = db[request.POST['dataset_id']]
		datav = collection.find( { } )
		pd.set_option('display.max_columns', None)

		data = pd.DataFrame(list(collection.find({selecteddatacol:{"$exists":True}})))
		valc=data[selecteddatacol]
		valc_list = valc.tolist()
		valc_fltlist = [float(i) for i in valc_list]
		print("val converted data col==>>",valc_fltlist)

		if selectedtest == 'Shapiro-Wilk Test':
			# Example of the Shapiro-Wilk Normality Test
			from scipy.stats import shapiro
			data = valc_fltlist
			stat, p = shapiro(data)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably Gaussian')
				gaussian_result = 'Probably Gaussian'
			else:
				print('Probably not Gaussian')
				gaussian_result = 'Probably not Gaussian'

			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"gaussian_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['gaussian_result'] = gaussian_result
			responseData['summary']=  describeDict




			print(responseData)
		elif selectedtest == 'D’Agostino’s K^2 Test':
			# Example of the D'Agostino's K^2 Normality Test
			from scipy.stats import normaltest
			data = valc_fltlist
			stat, p = normaltest(data)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably Gaussian')
				gaussian_result = 'Probably Gaussian'
			else:
				print('Probably not Gaussian')
				gaussian_result = 'Probably not Gaussian'

			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"gaussian_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['gaussian_result'] = gaussian_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Anderson-Darling Test':
			# Example of the Anderson-Darling Normality Test
			from scipy.stats import anderson
			data = valc_fltlist
			result = anderson(data)
			print('stat=%.3f' % (result.statistic))
			for i in range(len(result.critical_values)):
				sl, cv = result.significance_level[i], result.critical_values[i]
				if result.statistic < cv:
					print('Probably Gaussian at the %.1f%% level' % (sl))
				else:
					print('Probably not Gaussian at the %.1f%% level' % (sl))
		elif selectedtest == 'Pearson’s Correlation Coefficient':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Pearson's Correlation test
			from scipy.stats import pearsonr
			data1 = valc_fltlist

			print(data1)
			data2 = valc2_fltlist
			stat, p = pearsonr(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably independent')
				relationship_result = 'Probably Independent'
			else:
				print('Probably dependent')
				relationship_result = 'Probably Dependent'
			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"relationship_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['relationship_result'] = relationship_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Spearman’s Rank Correlation':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Pearson's Correlation test
			from scipy.stats import spearmanr
			data1 = valc_fltlist

			print(data1)
			data2 = valc2_fltlist
			stat, p = spearmanr(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably independent')
				relationship_result = 'Probably Independent'
			else:
				print('Probably dependent')
				relationship_result = 'Probably Dependent'
			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"relationship_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['relationship_result'] = relationship_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Kendall’s Rank Correlation':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Pearson's Correlation test
			from scipy.stats import kendalltau
			data1 = valc_fltlist

			print(data1)
			data2 = valc2_fltlist
			stat, p = kendalltau(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably independent')
				relationship_result = 'Probably Independent'
			else:
				print('Probably dependent')
				relationship_result = 'Probably Dependent'
			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"relationship_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['relationship_result'] = relationship_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Student’s t-test':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Student's t-test
			from scipy.stats import ttest_ind
			data1 = valc_fltlist
			print(data1)
			data2 = valc2_fltlist
			stat, p = ttest_ind(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably the same distribution')
				distribution_result = 'Probably Same Distribution'
			else:
				print('Probably different distributions')
				distribution_result = 'Probably Different Distributions'


			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"distribution_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['distribution_result'] = distribution_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Paired Student’s t-test':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Paired Student's t-test
			from scipy.stats import ttest_rel
			data1 = valc_fltlist
			print(data1)
			data2 = valc2_fltlist
			stat, p = ttest_rel(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably the same distribution')
				distribution_result = 'Probably Same Distribution'
			else:
				print('Probably different distributions')
				distribution_result = 'Probably Different Distributions'


			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"distribution_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['distribution_result'] = distribution_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Mann-Whitney U Test':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Mann-Whitney U Test
			from scipy.stats import mannwhitneyu
			data1 = valc_fltlist
			print(data1)
			data2 = valc2_fltlist
			stat, p = mannwhitneyu(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably the same distribution')
				distribution_result = 'Probably Same Distribution'
			else:
				print('Probably different distributions')
				distribution_result = 'Probably Different Distributions'


			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"distribution_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['distribution_result'] = distribution_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Wilcoxon Signed-Rank Test':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Wilcoxon Signed-Rank Test
			from scipy.stats import wilcoxon
			data1 = valc_fltlist
			print(data1)
			data2 = valc2_fltlist
			stat, p = wilcoxon(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably the same distribution')
				distribution_result = 'Probably Same Distribution'
			else:
				print('Probably different distributions')
				distribution_result = 'Probably Different Distributions'


			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"distribution_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['distribution_result'] = distribution_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Kruskal-Wallis H Test':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Kruskal-Wallis H Test
			from scipy.stats import kruskal
			data1 = valc_fltlist
			print(data1)
			data2 = valc2_fltlist
			stat, p = kruskal(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably the same distribution')
				distribution_result = 'Probably Same Distribution'
			else:
				print('Probably different distributions')
				distribution_result = 'Probably Different Distributions'


			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"distribution_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['distribution_result'] = distribution_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Friedman Test':
			# Example of the Anderson-Darling Normality Test
			selecteddatacol2 = request.POST['selecteddatacol2']
			print("2nd Data = ", request.POST['selecteddatacol2'])
			collection2 = db[request.POST['dataset_id2']]
			print("2nd Dataset ID = ", request.POST['dataset_id2'])

			datav2 = collection2.find( { } )
			pd.set_option('display.max_columns', None)
			data2 = pd.DataFrame(list(collection2.find({selecteddatacol2:{"$exists":True}})))
			valc2=data2[selecteddatacol2]
			valc2_list = valc2.tolist()
			valc2_fltlist = [float(i) for i in valc2_list]
			print("val converted data col 2==>>",valc2_fltlist)

			# Example of the Friedman Test
			from scipy.stats import friedmanchisquare
			data1 = valc_fltlist
			print(data1)
			data2 = valc2_fltlist
			stat, p = friedmanchisquare(data1, data2)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably the same distribution')
				distribution_result = 'Probably Same Distribution'
			else:
				print('Probably different distributions')
				distribution_result = 'Probably Different Distributions'


			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"distribution_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['distribution_result'] = distribution_result
			responseData['summary']=  describeDict

			print(responseData)
		elif selectedtest == 'Augmented Dickey-Fuller Unit Root Test':
			# Example of the D'Agostino's K^2 Normality Test
			from statsmodels.tsa.stattools import adfuller
			data = valc_fltlist
			stat, p, lags, obs, crit, t = adfuller(data)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably not Stationary')
				stationary_result = 'Probably not Stationary'
			else:
				print('Probably Stationary')
				stationary_result = 'Probably Stationary'

			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"stationary_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['stationary_result'] = stationary_result
			responseData['summary']=  describeDict
		elif selectedtest == 'Kwiatkowski-Phillips-Schmidt-Shin':
			# Example of the Kwiatkowski-Phillips-Schmidt-Shin test
			from statsmodels.tsa.stattools import kpss
			data = valc_fltlist
			stat, p, lags, crit = kpss(data)
			stat = round(stat,3)
			p = round(p,3)
			print('stat=%.3f, p=%.3f' % (stat, p))
			if p > 0.05:
				print('Probably not Stationary')
				stationary_result = 'Probably not Stationary'
			else:
				print('Probably Stationary')
				stationary_result = 'Probably Stationary'

			responseData = {
	           	'summary':result,
				'selectedtest': selectedtest,
	        }

			describeDict = {
				"stat" : "",
				"p" : "",
				"stationary_result" : "",
			}

			describeDict['stat'] = stat
			describeDict['p'] = p
			describeDict['stationary_result'] = stationary_result
			responseData['summary']=  describeDict
		print ('$$%$%$%$%',responseData)

	return JsonResponse(responseData)

#calculaateAnalytics
def calculateAnalytics(request):
	print('Hiiiiiiiiii')
	if request.method == 'POST':
		result = 0
		res = 0
		print("In Post Method")
		fieldsArr = []
		print(fieldsArr)
		selectedgroupname = request.POST['selectedgroup']
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
		datav = collection.find( { } )
		pd.set_option('display.max_columns', None)

		#########Anova Calcs Starts from here########
		datag = pd.DataFrame(list(collection.find({selectedgroup:{"$exists":True}})))
		datac = pd.DataFrame(list(collection.find({selecteddatacol:{"$exists":True}})))
		#print ("DATAG==>")
		#print(datag)
		#print ("DATAC==>")
		#print(datac)
		print("type datag###", type(datag))

		g=datag[selectedgroup]

		c=datac[selecteddatacol]
		print("Grouped data col====>")
		print(g)
		print("Val data col====>")
		print(c)

		k=len(pd.unique(g))
		print("unique groups==>",pd.unique(g))

		N=len(datag.values)
		print("Datag values ==>>",datag.values)
		n=datag.groupby(g).size()[0]
		print("data grouped==>",datag.groupby(g))
		print("k==>",k)
		print("N==>",N)
		print("n==>",n)

		#degrees of freedom
		df_between = k-1
		df_within = N-k
		df_total = df_between + df_within
		print("df_between==>",df_between)
		print("df_within==>",df_within)
		print("df_total==>",df_total)

		print('Group=>',selectedgroup)
		# c_data= c.convert_objects(convert_numeric=True)

		c_data = pd.to_numeric(c, errors='coerce')

		ss_between = (sum(c_data.groupby(g).sum()**2)/n) - (c_data.sum()**2)/N
		print("ss_between==>",ss_between)

		sum_y_squared = sum([value**2 for value in c_data.values])
		#print(sum_y_squared)

		ss_within = sum_y_squared - sum(c_data.groupby(g).sum()**2)/n
		print("ss_within==>",ss_within)

		ss_total = sum_y_squared - (c_data.sum()**2)/N
		print("ss_total==>",ss_total)


		#mean square
		ms_between = ss_between/df_between
		ms_within = ss_within/df_within
		print("ms_between==>",ms_between)
		print("ms_within==>",ms_within)

		#calculating the f-ration
		f = ms_between/ms_within

		f = truncate(f,5)
		print("Value of F ", f)
		#calculating p-value
		p=stats.f.sf(f, df_between, df_within)
		p = truncate(p,5)
		#effect sizes
		eta_square = ss_between/ss_total
		eta_square = truncate(eta_square,5)
		omega_square = (ss_between - (df_between * ms_within))/(ss_total + ms_within)
		omega_square = truncate(omega_square,5)

		og = list(datag.loc[:,selectedgroup])
		oc = list(datac.loc[:,selecteddatacol])

		xx = pd.DataFrame(og,oc)
		print("omegasquare==>>", omega_square)
		csv = pd.DataFrame.to_csv(xx)
		#print(csv)
		sd = pd.read_csv(StringIO(csv))
		#print(sd)
		#print(selectedgroup)
		#cc = xx.columns
		#print(c)
		#ls=sd.describe()
		#ndf=pd.DataFrame({'':[f, p, eta_squared, omega_squared]}, index='f p eta_squared omega_squared'.split())
		ndf = pd.DataFrame({'f':f, 'p':p, 'eta_square':eta_square, 'omega_square':omega_square}, index=[0])
		#n_ndf = ndf.to_frame()
		#df = pd.DataFrame([{'pi':pi, 'e':e, 'phi':phi}])
		#print("NDF",ndf )
		#print("NDF Class===>>>",type(ndf) )
		csvn=pd.DataFrame.to_csv(ndf)

		nndf=pd.read_csv(StringIO(csvn))

		nndf_t = nndf/len(nndf)

		#nndf_data= nndf.convert_objects(convert_numeric=True)
		print("####ndf type", type(ndf.loc['0':,"omega_square"]))
		print("####nndf type", type(nndf.loc['0':,"omega_square"]))

		print("####nndf_t type", type(nndf_t))


		responseData = {
           	'summary':result,
			'fieldData':og,
			'selectedgroup': request.POST['selectedgroup']
        }

		describeDict = {
			"f" : "",
			"p" : "",
			"eta_square" : "",
			"omega_square":"",
		}
		#print(request.POST['selectedgroup'])
		if request.POST['selectedmethod'] == 'anova':

			describeDict['f'] = nndf_t.iloc[0]['f']
			describeDict['p'] = nndf_t.iloc[0]['p']
			describeDict['eta_square'] = nndf_t.iloc[0]['eta_square']
			describeDict['omega_square'] = nndf_t.iloc[0]['omega_square']
			responseData['summary']=  describeDict

		print ('$$%$%$%$%',responseData)


		return JsonResponse(responseData)


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier



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
		dec_p = 3
		print(request.POST['selectedfield'])
		if request.POST['selectedmethod'] == 'describe':

			med = sd.median()
			med1 = med.to_frame()
			med1 = med1.iloc[1][0]
			med1 = med1.tolist()
			med1 = truncate(med1,dec_p)

			ske = sd.skew()
			ske1 = ske.to_frame()
			ske1 = ske1.iloc[1][0]
			ske1 = ske1.tolist()
			tskew1 = truncate(ske1,dec_p)

			ls = sd.describe()
			print("LS",ls)
			count = ls.loc["count","0"]

			mean = ls.loc["mean","0"]
			mean = mean.tolist()
			mean = truncate(mean, dec_p)
			print(mean)

			std = ls.loc["std","0"]
			std = std.tolist()
			std = truncate(std, dec_p)

			kurt = sd.kurtosis()
			kurt1 = kurt.to_frame()
			kurt1 = kurt1.iloc[1][0]
			kurt1 = kurt1.tolist()
			kurt1 = truncate(kurt1,dec_p)

			describeDict['count'] = count
			describeDict['mean'] = mean
			describeDict['std'] = std
			describeDict['min'] = ls.loc["min","0"]
			describeDict['median'] = med1
			describeDict['skewness'] = tskew1
			describeDict['kurtosis'] = kurt1
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


def hypoList(request):
	msg="inside HypoLIST"
	client = MongoClient()
	print(client.list_database_names())
	db = client.hypoDatadb
	print("collections in your dataset",db.list_collection_names())
	collection_names = db.list_collection_names()
	print(type(collection_names))
	print(*collection_names, sep='\n')
	try:
		listObj=[]
		usr=str(request.user)
		print('list0')
		hypoList= hypothetical.objects.filter(user_id=request.user.id).values()
		print("hypolist",hypoList)
		if len(hypoList) > 0:
			for i in range(len(hypoList)):
				listObj.append(hypoList[i])
				print("%%%%",listObj[i])
		return JsonResponse(listObj,safe=False)
	except:
		msg = 'error while getting process list'
		print(msg)
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
