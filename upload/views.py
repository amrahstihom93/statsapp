import pymysql
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv, re, tablib, json, pymongo, ast, pprint, datetime
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from process.models import Process, Process_List
from django.contrib.auth.models import User
import pandas as pd
from upload.models import Dataset, Dataset_List
from upload.forms import DocumentForm

from messytables import CSVTableSet, XLSTableSet, type_guess, types_processor, headers_guess, headers_processor, \
    offset_processor, any_tableset


def home(request):
    documents = Dataset.objects.all()
    return render(request, 'core/home.html', {'documents': documents})


@csrf_exempt
def submitFiletype(request):
    if request.method == 'POST':
        print(request.POST)
        success_msg = ''
        success_msg = 'successful'
    return HttpResponse(success_msg)


# for testing dynamic collection creation in mongo
def makeCol(request):
    client = MongoClient()
    db = client.datasetData
    col = db.new
    cname = request.POST['colName']
    post = {
        "author": "Mike",
        "text": "My first  post!",
        "tags": ["mongodb", "python", "pymongo"]
    }
    id = col.insert_one(post).inserted_id
    print(id)
    col = db[cname]
    post = {
        "author": "VIV",
        "text": "My 2nd blog post!",
        "tags": ["mongodb", "python", "pymongo"]
    }
    id = col.insert_one(post).inserted_id
    print(id)


def upload1(request):
    data = tablib.Dataset()
    #	imported_data = data.load(open('data.csv').read())
    #	print(imported_data.export('json'))
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        print(request)
        string = myfile.read().decode('utf-8')
        data.csv = string
        #	print(data)
        json_data = data.export('json')
        #	print(type(json_data))
        #	print(json_data)
        doc = Dataset()
        doc.dataset_name = 'd2'
        doc.data = json_data
        doc.save()
        # handle_files(string)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #	data = [row for row in csv.reader(myfile.read().splitlines())]

        # you can use the re library --> import re
        # splits along new line
        return render(request, 'test-csv.html', {
            'uploaded_file_url': uploaded_file_url,
            'filename': filename,
            'fileData': string,
        })
    # file_data = myfile.read()
    # v = { 'foo': 'bar'}
    # reader = csv.reader(myfile)
    # i = 0
    # ob=[]
    # for row in reader:
    #	ob[i]= row
    # print('hello')
    # return HttpResponse("filename is :"+ str(filename)+"<h1>Data is </h1>" +"<p>"+str(file_data) +str(ob)+"</p>")
    return render(request, 'upload_preview.html')


def saveDataInMongo(json_data, datasetId):
    client = MongoClient()
    db = client.datasetDatadb
    col = db[datasetId]
    convertedData = ast.literal_eval(json_data)
    result = col.insert_many(convertedData)


#    print('mamu')
#    print(result.inserted_ids)
#    print(col.find_one({'_id': result.inserted_ids[0]}))
#	print(col.find_one({'_id': result.inserted_ids[0]}))

def xsaveDataInMongo(json_data, datasetCol, username):
    dataObj = []
    client = MongoClient()
    db = client.datasetDatadb
    #	print("db",db)
    #	print(datasetCol)
    collection = db['rowData']
    #	print(collection)
    convertedData = ast.literal_eval(json_data)
    for data in convertedData:
        obj = {}
        obj['user_id'] = username
        obj['dataset_id'] = datasetCol
        obj['name'] = 'data'
        obj['data'] = data
        dataObj.append(obj)
    # print(obj)
    #	print("jsondata")
    print('data obj', dataObj)
    #	print(json_data)
    #	print(collection)
    #	print(db.collection.find({"name":"headers"}))
    #	print(convertedData[0])
    #	print(type(convertedData))
    #	print(convertedData)
    result = collection.insert_many(dataObj)


#	print(result.inserted_ids)
#	print(collection.find_one({'dataset_id': result.inserted_ids[0]}))
#	print(json_data[1])
#	for p in collection.find({'dataset_id': datasetCol, 'user_id': username}):
#		pprint.pprint(p)

def saveHeaderInMongo(datasetName, headersList, dataTypes, username, d_id):
    client = MongoClient()
    db = client.datasetDatadb
    collection = db['headersData']
    print(collection)
    j = 0
    k = 0
    headers = {}
    headers['name'] = 'headers'
    headers['user_id'] = username
    headers['dataset_id'] = str(datasetName)
    headers['d_id'] = d_id
    for type in dataTypes:
        dataTypes[k] = str(dataTypes[k])
        k = k + 1

    for header in headersList:
        headers[header] = dataTypes[j]
        j = j + 1
    # print(types)
    #	print("healist class")
    #	print(headersList)
    # print(type(headers))
    print(headers)
    #	json_headers = json.dumps(headers)
    #	convertedData = ast.literal_eval(json_headers)
    #	print(type(json_headers))
    print('header_id')
    headers_id = collection.insert_one(headers)
    print(headers_id.inserted_id)


#	print(collection.find_one({'dataset_id':'vik12'}))

def changeDataTypeInMongo(request):
    success = ''
    dataSet_id = request.POST['dname']
    usr_id = str(request.user)
    typeOb = request.POST['changedDataType']
    print(request.POST)
    # print(collectionName)
    print(typeOb)
    print(type(typeOb))
    #	t = json.dumps(typeOb)
    convertedData = ast.literal_eval(typeOb)
    print(type(convertedData))
    print(convertedData)
    client = MongoClient()
    db = client.datasetDatadb
    collection = db['headersData']
    print(collection)
    #	json_datatype = json.dumps(typeObj)
    #	convertedData = ast.literal_eval(json_datatype)
    #	id = collection.insert_one(convertedData)
    #	print(id.inserted_id)
    #	updated_id = db.collection.update_one({
    #		'name': 'headers'
    #	},{
    #		'$set': convertedData
    #
    up = collection.find_one_and_update(
        {'dataset_id': dataSet_id, 'user_id': usr_id},
        {'$set': convertedData})
    print(up)
    print(collection.find_one({'dataset_id': dataSet_id, 'user_id': usr_id}))
    #	found = collection.find_one({'name':'headers'})
    #	print(found)
    #	print(updated_id.modified_count)
    if up != None:
        success = 'datatype has been saved'
    else:
        success = 'error in saving datatype'
    return HttpResponse(success, content_type="text/plain")


def isDuplicate(datasetName, processId, userId):
    datasetFromPostgresCount = Dataset.objects.filter(dataset_name=datasetName, process_id=processId,
                                                      user_id=userId).count()
    if datasetFromPostgresCount > 0:
        return True
    return False


def saveMySqlDataInMongo(all_data, d_id):
    tempdata = tablib.Dataset()
    tempdata.csv = all_data
    print('tempdata----')
    print(tempdata)
    print('alldata---\n'+ all_data)
    json_data = tempdata.export('json')
    print('shdjdkff-----------')
    print(json_data)
    saveDataInMongo(json_data, d_id)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        dataset_name = request.POST['datasetName']
        pro = request.POST['process_id']
        fileType = request.POST['fileType']
        dataInCsv = request.POST['allData']
        headersInCsv = request.POST['headers']
        print('operation----'+ headersInCsv)
        form = Dataset()
        form1 = Dataset_List()
        data = tablib.Dataset()
        fs = FileSystemStorage()
        d_id = 'DID' + dataset_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if fileType == 'mysql':
            typesInStr = request.POST['types']
            dataTypes = typesInStr.split(',')
            types = dataTypes
            headersInList = headersInCsv.split(',')
            print(types)
            print(type(request.POST['types']))
            print(type(types))
            saveHeaderInMongo(dataset_name, headersInList, dataTypes, str(request.user), d_id)
            saveMySqlDataInMongo(request.POST['allData'], d_id)
            print('------')
            uploaded_file_url = "NA"
        else:
            if isDuplicate(dataset_name, pro, request.user.id) == True:
                res = {
                    'isDuplicate' : True
                }
                return JsonResponse(res)
            data.csv = request.POST['allData']
            h = request.POST['headers']
            h = h.split(',')
            csv_file = request.FILES['myfile']
            if fileType == 'csv':
                table_set = CSVTableSet(csv_file)
            if fileType == 'xls':
                table_set = XLSTableSet(csv_file)
            row_set = table_set.tables[0]
            offset, headers = headers_guess(row_set.sample)
            row_set.register_processor(headers_processor(headers))
            row_set.register_processor(offset_processor(offset + 1))
            types = type_guess(row_set.sample, strict=True)
            dataTypeObj = {}
            for i in range(len(types)):
                dataTypeObj[data.headers[i]] = types[i]
            data.headers = h
            json_data = data.export('json')
            dataTypes = types
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)
            saveHeaderInMongo(dataset_name, data.headers, dataTypes, str(request.user), d_id)
            saveDataInMongo(json_data, d_id)
        process_obj = Process.objects.get(pk=request.POST['process_id'])
        user_obj = User.objects.get(pk=request.user.id)
        form.dataset_name = dataset_name
        form.data = dataInCsv
        form.document = uploaded_file_url
        form.user_id = user_obj
        form.process_id = process_obj
        form.dataset_id = d_id
        form.save()
        dataset_obj = Dataset.objects.get(dataset_id=form.dataset_id)
        form1.d_id = dataset_obj
        form1.u_id = user_obj
        form1.p_id = process_obj
        form1.save()
        responseData = {
            'fileData': dataInCsv,
            'datasetname': request.POST['datasetName'],
            'typesArray': types,
            'isDuplicate' : False
        }
        return JsonResponse(responseData)




@csrf_exempt
def xupload(request):
    print("in upload")
    print(request.user)
    usr = request.user
    id = request.user.id
    susr = str(usr)
    res = ''
    dataset_name = request.POST['datasetName']
    fileType = request.POST['fileType']
    # print(request.POST['process_id'])
    pro = request.POST['process_id']
    isDuplicate(dataset_name, pro, id)
    datasetFromPostgresCount = Dataset.objects.filter(dataset_name=dataset_name, process_id=pro, user_id=id).count()
    print("datasetFromPostgres")
    if datasetFromPostgresCount > 0:
        print(datasetFromPostgresCount)
        res = 'duplicate dataset'
        return HttpResponse(res)
    print('user')
    print(usr)
    if request.method == 'POST' and request.FILES['myfile']:
        process_id = request.POST['process_id']
        csv_file = request.FILES['myfile']
        #	form = DocumentForm(request.POST, request.FILES)
        form = Dataset()
        form1 = Dataset_List()
        data = tablib.Dataset()
        #	print(request.POST)
        #	print(request.POST['datasetName'])
        print("this is csv")
        print(csv_file)
        #	string = csv_file.read().decode('utf-8')
        print("this read string")
        #	print(string)
        #	print(request.POST['allData'])
        data.csv = request.POST['allData']
        h = request.POST['headers']
        h = h.split(',')
        #	print(data.csv)
        #	print(data.headers)
        #	fh = open('messy.csv', 'rb')
        fh = csv_file
        # Load a file object:
        if fileType == 'csv':
            table_set = CSVTableSet(fh)
        if fileType == 'xls':
            table_set = XLSTableSet(fh)
        # print("this is table set")
        #	print(table_set)

        # If you aren't sure what kind of file it is, you can use
        # any_tableset.
        # table_set = any_tableset(fh)
        # A table set is a collection of tables:
        row_set = table_set.tables[0]
        # A row set is an iterator over the table, but it can only
        # be run once. To peek, a sample is provided:
        # print(row_set.sample.next())

        # guess header names and the offset of the header:
        offset, headers = headers_guess(row_set.sample)
        row_set.register_processor(headers_processor(headers))

        # add one to begin with content, not the header:
        row_set.register_processor(offset_processor(offset + 1))
        # guess column types:
        types = type_guess(row_set.sample, strict=True)
        dataTypeObj = {}
        for i in range(len(types)):
            dataTypeObj[data.headers[i]] = types[i]
        # t = []
        #	for i in range(len(types)):
        #		print(types[i])
        #		t.append(types[i])
        # t[i] = types[i]
        #	print(t)
        # and tell the row set to apply these types to
        # each row when traversing the iterator:
        #	row_set.register_processor(types_processor(types))

        # now run some operation on the data:
        # for row in row_set:
        # print(row)
        data.headers = h
        #	print(data.csv)
        #	print(string)
        json_data = data.export('json')
        print('jsonheaders')
        print(json_data)
        dataTypes = types
        saveHeaderInMongo(request.POST['datasetName'], data.headers, dataTypes, susr)
        saveDataInMongo(json_data, request.POST['datasetName'], susr)
        #	print(type(json_data))
        #	print(json_data)
        process_obj = Process.objects.get(pk=request.POST['process_id'])
        user_obj = User.objects.get(pk=request.user.id)
        form.dataset_name = request.POST['datasetName']
        form.data = data.csv
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        uploaded_file_url = fs.url(filename)
        form.document = uploaded_file_url
        form.user_id = user_obj
        form.process_id = process_obj
        form.dataset_id = 'DID' + form.dataset_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        form.save()
        dataset_obj = Dataset.objects.get(dataset_id=form.dataset_id)
        form1.d_id = dataset_obj
        form1.u_id = user_obj
        form1.p_id = process_obj
        form1.save()

        typesString = str(types)
        slicedTypes = typesString[1:len(typesString) - 1]
        #	print(slicedString)
        responseData = {
            'uploaded_file_url': uploaded_file_url,
            'fileData': data.csv,
            'datasetname': request.POST['datasetName'],
            'typesArray': types
        }
        return JsonResponse(responseData)


def delDatasetFromMongo(user_id, dataset_id):
    print("in delDatasetFromMongo")
    print(dataset_id)
    client = MongoClient()
    db = client.datasetDatadb
    rowCollection = db['rowData']
    headersCollection = db['headersData']
    res = False
    rowCount = rowCollection.count({'user_id': str(user_id), 'dataset_id': dataset_id})
    print(rowCount)
    try:
        rowCount = rowCollection.count({'user_id': str(user_id), 'dataset_id': dataset_id})
        print(rowCount)
        rowCollection.delete_many({'user_id': str(user_id), 'dataset_id': dataset_id})
        rowCount = rowCollection.count({'user_id': str(user_id), 'dataset_id': dataset_id})
        print("after delete")
        print(rowCount)
        res = True
    except:
        print("can't data delete from mongo")
        res = False

    try:
        rowCount = headersCollection.count({'user_id': str(user_id), 'dataset_id': dataset_id})
        print(rowCount)
        headersCollection.delete_one({'user_id': str(user_id), 'dataset_id': dataset_id})
        rowCount = headersCollection.count({'user_id': str(user_id), 'dataset_id': dataset_id})
        print("after delete")
        print(rowCount)
        res = True
    except:
        print("can't headers delete from mongo")
        res = False
    return res


# Function to Delete Dataset from Mongo and Postgres
def deleteDataset(request, dataset_name):
    print("in del dataset")
    res = ''
    print(dataset_name)
    usr = request.user
    try:
        print("row to delete")
        rowToDelete = Dataset.objects.get(dataset_name=dataset_name)
        print('rowin', rowToDelete.dataset_id)
        deleteFromDatasetList = Dataset_List.objects.get(d_id=rowToDelete.dataset_id)
        #	dataSet_id = rowToDelete.dataSet_id
        print('ajeeb', deleteFromDatasetList)
        print(rowToDelete.dataset_id)
        print("row to delete1")
        deleteFromDatasetList.delete()
        rowToDelete.delete()
    except:
        print("someting wrong")
        res = 'Dataset doesnot Exist'
        return HttpResponse(res)
    res = delDatasetFromMongo(usr, dataset_name)
    if res == True:
        res = 'Delete successful'
    else:
        res = 'partial delete'
    return HttpResponse(res)


def giveDatasetName(request):
    if request.method == 'POST':
        fetchedDatasetName = ''
        datasetId = request.POST['dataset_id']
        fetchedDatasetName = Dataset.objects.get(pk=datasetId)
        print(fetchedDatasetName)
        return HttpResponse(fetchedDatasetName)


def mysqlconnect(request):
    if request.method == 'POST':
        tableList = []
        dbUrl = request.POST['dbUrl']
        dbUserName = request.POST['userName']
        dbName = request.POST['dbName']
        tbName = request.POST['tbName']
        dbPassword = request.POST['password']
        dbPort = request.POST['port']
        print('here in mysql connect --------------')
        print(dbUrl)
        print(dbUserName)
        print(dbPassword)
        print(type(dbPort))
        print(dbPort)
        cn='Column Name'
        dt= 'datat type'
        conn = pymysql.connect(host=dbUrl,
                               port=int(dbPort),
                               database =dbName,
                               user=dbUserName,
                               password=dbPassword)
        Query = 'Select * from %s' % tbName
        queryColumnName= 'Select column_name {!r}, data_type {!r} FROM information_schema.columns WHERE TABLE_NAME = {!r}'.format(cn,dt,tbName)
        # queryColumnName= 'Select column_name \''+ cn + '\', data_type '+ dt + ' FROM information_schema.columns WHERE TABLE_NAME = '+ tbName
        print('header query ----------------')
        print(queryColumnName)
        headerData = pd.read_sql_query(queryColumnName, conn)
        print('hey     ----------------------------------------------------------')
        print(headerData)
        data = pd.read_sql_query(Query, conn)

    # code to insert data in mongodbusing dataframe
    #   client = MongoClient()
    #   db = client.datasetDatadb
    #   postd = db.postd123
    #   data_json = json.loads(data.to_json(orient='records'))
    #   postd.remove()
    #   postd.insert(data_json)
        csv = pd.DataFrame.to_csv(data, index=False )
        types = pd.DataFrame.to_csv(headerData ,index=False )


        response = {
            'csv': csv,
            'types': types
        }
        return JsonResponse(response)
