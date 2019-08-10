import pymongo
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from upload.models import Dataset
from .models import visualization
from django.contrib.auth.models import User
import json, datetime

# Create your views here.
def chart(request):
    return render(request, 'chart.html')


def makechart(request, graph_type, dataset_name):
    client = MongoClient()
    db = client.datasetDatadb
    collection = db[dataset_name]
    fields = collection.find_one({"name": "headers"})
    fields_list = list(fields.values())
    del fields_list[0:2]
    return render(request, 'makechart.html', {
        'dataset_name': dataset_name,
        'fields': fields_list
    })


def get_data(request, graph_type, dataset_name):
    #	labels = ["India", "Sri lanka", "Austria", "England", "Greenland"]
    #	default_items = [23,2,3,12,2]
    labels = []
    default_items = []
    if request.method == 'POST':
        print(request.POST['x_axis_value'])
        print(request.POST['y_axis_value'])
        x = request.POST['x_axis_value']
        y = request.POST['y_axis_value']
        client = MongoClient()
        db = client.datasetDatadb
        collection = db[dataset_name]
        print(y)
        dataFromMongo = collection.find({y: {"$exists": True}})
        for doc in dataFromMongo:
            default_items.append(doc[y])
        dataFromMongo = collection.find({x: {"$exists": True}})
        for doc in dataFromMongo:
            labels.append(doc[x])
            #		print(dataFromMongo)
    print("ght")
    print(dataset_name)
    print(graph_type)
    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)


@csrf_exempt
def visualization_data(request, dataset_name):
    print("in visualization_data backend")
    print(request.POST)
    labels = []
    default_items = []
    x = request.POST['x_value']
    y = request.POST['y_value']
    print("x is ")
    print(x)
    print("y is ")
    print(y)
    client = MongoClient()
    db = client.datasetDatadb
    collection = db[dataset_name]
    print(y)
    dataFromMongo = collection.find({y: {"$exists": True}})
    for doc in dataFromMongo:
        default_items.append(doc[y])
    dataFromMongo = collection.find({x: {"$exists": True}})
    for doc in dataFromMongo:
        labels.append(doc[x])
    print(dataset_name)
    data = {
        "labels": labels,
        "default": default_items,
    }
    return JsonResponse(data)


def get_visualization(request, dataset_name):
    client = MongoClient()
    db = client.datasetDatadb
    collection = db[dataset_name]
    fields = collection.find_one({"name": "headers"})
    fields_list = list(fields.values())
    del fields_list[0:2]
    return render(request, 'visualization.html', {
        'dataset_name': dataset_name,
        'fields': fields_list
    })


# After adding dataset table in visualization tab
def getDataset(request):
    print("in get Dataset")
    msg = ''
    listObj = []
    usr = str(request.user)
    # print('usr',usr.id)
    try:
        print('indfg')
        datasetsList = Dataset.objects.filter(user_id=request.user.id).values()
        # datasetsList = Document.objects.all().values()
        #	print(datasetsList)
        #	print('23we')
        if len(datasetsList) > 0:
            print('len', len(datasetsList))
            for i in range(len(datasetsList)):
                listObj.append(datasetsList[i])
                print(datasetsList[i])
                print(datasetsList[i]['dataset_id'])
        return JsonResponse(listObj, safe=False)
    except:
        msg = 'error while getting datasets'
    return HttpResponse(msg)


def getGraphFields(request):
    print("in get graph fields")
    fieldsArr = []
    dataset_id = request.POST['dName']
    print(dataset_id)
    susr = str(request.user)
    client = MongoClient()
    db = client.datasetDatadb
    collection = db['headersData']
    fieldsDoc = collection.find_one({'user_id': susr, 'dataset_id': dataset_id})
    print(fieldsDoc)
    fieldsDoc.pop('_id', None)
    fieldsDoc.pop('dataset_id', None)
    fieldsDoc.pop('user_id', None)
    fieldsDoc.pop('name', None)
    print(fieldsDoc)
    fieldsArr = list(fieldsDoc.keys())
    # del fieldsArr[0:4]
    print(fieldsArr)
    return JsonResponse(fieldsArr, safe=False)


def getGraphData(request):
    print("in visualization ")
    usr = str(request.user)
    labels = []
    default_items = []
    dataset_id = request.POST['dtName']
    x = request.POST['x_value']
    y = request.POST['y_value']
    datasetID = Dataset.objects.get(dataset_name=dataset_id, user_id=request.user.id)
    print('datasetId')
    print(datasetID.dataset_id)
    col = datasetID.dataset_id
    client = MongoClient()
    db = client.datasetDatadb
    collection = db[col]
    dataFromMongo = collection.find({})
    print('graph dta-------')
    print(dataFromMongo)
    for doc in dataFromMongo:
        print(doc)
        default_items.append(doc[y])
        labels.append(doc[x])
    data = {
        "labels": labels,
        "defaultData": default_items,
    }
    print(data)
    return JsonResponse(data)


def saveVisualization(request):
    vForm = visualization()
    json_data = {}
    data = {}
    if request.method == 'POST':
        vForm.visualization_name = request.POST['visualization_name']
        vForm.type = request.POST['graphType']
        data = request.POST['data']
        json_data = json.loads(data)
        vForm.parameters = json_data
        dataset_obj = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
        user_obj = User.objects.get(pk=request.user.id)
        vForm.user_id = user_obj
        vForm.dataset_id = dataset_obj
        vForm.visualization_id = 'vid' + request.POST['visualization_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        vForm.save()
        msg = 'saved successfully'
        return HttpResponse(msg)
    msg = 'error'
    return HttpResponse(msg)


def getVisualizationList(request):
    usr = str(request.user)
    listObj = []
    try:
        print('in visualList')
        visualList = visualization.objects.filter(user_id=request.user.id).values()
        if len(visualList) > 0:
            for i in range(len(visualList)):
                listObj.append(visualList[i])
                print('xxx', visualList[i])
        return JsonResponse(listObj, safe=False)
    except:
        msg = 'error while getting datasets'
    return HttpResponse(msg)


def delVisualization(request, id):
    res = ''
    try:
        visualizationToDelete = visualization.objects.get(pk=id)
        visualizationToDelete.delete()
        res = 'delete successful'
    except:
        res = 'delete unsuccessful'
    return HttpResponse(res)


def editVisualisation(request):
    json_data = {}
    data = {}
    print('hey from edit visual')
    print(request.POST)
    try:
        if request.method == 'POST':
            id = request.POST['visualization_id']
            vForm = visualization.objects.get(pk=id)
            visualization_name = request.POST['visualization_name']
            if visualization_name != '':
                vForm.visualization_name = visualization_name
            vForm.id = request.POST['visualization_id']
            data = request.POST['data']
            json_data = json.loads(data)
            vForm.parameters = json_data
            print('parameters from visualisation', vForm.parameters)
            vForm.save()
            msg = 'saved successfully'
            return HttpResponse(msg)
    except:
        msg = 'something went wrong while updating'
        return HttpResponse(msg)
