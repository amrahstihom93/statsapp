import pymongo
from pymongo import MongoClient
import json, datetime
import pandas as pd
from django.contrib.auth.models import User
from pprint import pprint
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from process.models import Process, Process_List
from .models import fmea

# Create your views here.
def qtools(request):
    print("Quality Tools DUDE!!!")
    return render(request, 'qtools.html')

def opptracker(request):
    return render(request, 'opptrack.html')
def fmeaList(request):
    msg = "insideListFmea"
    client = MongoClient()
    print(client.list_database_names())
    collection_name = "fmeaData"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    db = client.fmeaDatadb
    print("collections in your dataset",db.list_collection_names())
    collection_names = db.list_collection_names()
    print(type(collection_names))
    print(*collection_names, sep='\n')

    try:
        listObj=[]
        usr=str(request.user)
        print('list0')
        # list = Process.objects.filter(user_id=usr.id).values()
        fmeaList= fmea.objects.filter(user_id=request.user.id).values()
        # fmeaObj=fmea.objects.filter(fmea_name).values()
        print("fmealist",fmeaList)
        # print("fmeaObj",fmeaObj)
        # list = Process.objects.get(user_id=request.user.id).values()
        # print('list',list)
        if len(fmeaList) > 0:
            for i in range(len(fmeaList)):
                listObj.append(fmeaList[i])
                print("%%%%",listObj[i])
            # res = [ sub['fmea_name'] for sub in listObj]
            # print(res)
        return JsonResponse(listObj,safe=False)
    except:
        msg = 'error while getting process list'
        print(msg)
    return HttpResponse(msg)
def saveFMEA(request):

    client =MongoClient()

    db = client.fmeaDatadb
    print(client.list_database_names())
    print(db.list_collection_names())
    collection_name = "fmeaData"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    col = db[collection_name]
    print('into saveFMEA')
    vForm = fmea()
    json_data = {}
    data = {}
    msg = 'hi'
    if request.method == 'POST':
        vForm.fmea_name= request.POST['fmeaName']
        # vForm.selectedProcess = request.POST['selectedProcess']
        # print("selectedProcess", vForm.selectedProcess)
        vForm.parameters = request.POST['fmeaparam']
        print("parameters",type(vForm.parameters))
        datdoc = json.loads(vForm.parameters)
        print("datadocument", datdoc)
        vForm.parameters=""
        user_obj = User.objects.get(pk=request.user.id)
        vForm.user_id=user_obj
        vForm.fmea_sheetid = collection_name
        process_obj = Process.objects.get(pk=request.POST['process_id'])
        vForm.process_id = process_obj
        print("fmeaname",vForm.fmea_name)
        print("fmea_sheetid", vForm.fmea_sheetid)
        print("userid",vForm.user_id)
        print("processId", vForm.process_id)
        print('hi from save all')

        colId=col.insert_many(datdoc)
        print(colId.inserted_ids)
        vForm.save()
        msg='saved successfully'
        return HttpResponse(msg)
    msg = 'error while saving fmeasheet'
    return HttpResponse(msg)
