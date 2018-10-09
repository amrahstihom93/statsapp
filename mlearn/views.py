from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pymongo
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
	return HttpResponse(request)
