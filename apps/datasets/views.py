import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv, tablib, json, ast, datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.processes.models import Process, Process_List
from django.contrib.auth.models import User
import pandas as pd
from apps.datasets.models import Dataset, Dataset_List, ColumnMeta
from apps.datasets.forms import DocumentForm

logger = logging.getLogger(__name__)


def home(request):
    documents = Dataset.objects.all()
    return render(request, 'core/home.html', {'documents': documents})


@csrf_exempt
def submitFiletype(request):
    if request.method == 'POST':
        return HttpResponse('successful')
    return HttpResponse('')


# Stub: makeCol no longer needed (was a MongoDB test)
def makeCol(request):
    return HttpResponse('MongoDB removed — no longer needed')


def isDuplicate(datasetName, processId, userId):
    return Dataset.objects.filter(
        dataset_name=datasetName,
        process_id=processId,
        user_id=userId
    ).exists()


def _infer_column_types(df):
    """Infer column data types from a pandas DataFrame."""
    type_map = {}
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]):
            type_map[col] = 'integer'
        elif pd.api.types.is_float_dtype(df[col]):
            type_map[col] = 'decimal'
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            type_map[col] = 'datetime'
        else:
            type_map[col] = 'string'
    return type_map


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        dataset_name = request.POST.get('datasetName', '')
        pro = request.POST.get('process_id', '')
        fileType = request.POST.get('fileType', 'csv')
        dataInCsv = request.POST.get('allData', '')
        headersInCsv = request.POST.get('headers', '')

        d_id = 'DID' + dataset_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if fileType == 'mysql':
            # MySQL import path — headers & data come in as strings
            headersInList = headersInCsv.split(',')
            typesInStr = request.POST.get('types', '')
            dataTypes = typesInStr.split(',')
            df = pd.read_csv(pd.io.common.StringIO(dataInCsv))
            json_data = json.loads(df.to_json(orient='records'))
            type_map = {h: t for h, t in zip(headersInList, dataTypes)}
            uploaded_file_url = "NA"
        else:
            if isDuplicate(dataset_name, pro, request.user.id):
                return JsonResponse({'isDuplicate': True})

            csv_file = request.FILES.get('myfile')
            if csv_file is None:
                return JsonResponse({'error': 'No file uploaded'}, status=400)

            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            uploaded_file_url = fs.url(filename)

            try:
                if fileType == 'xls' or fileType == 'xlsx':
                    df = pd.read_excel(csv_file)
                else:
                    csv_file.seek(0)
                    df = pd.read_csv(csv_file)
            except Exception as e:
                logger.error(f"Error parsing file: {e}")
                return JsonResponse({'error': 'Could not parse file'}, status=400)

            json_data = json.loads(df.to_json(orient='records'))
            type_map = _infer_column_types(df)

        try:
            process_obj = Process.objects.get(pk=pro)
        except Process.DoesNotExist:
            return JsonResponse({'error': 'Process not found'}, status=400)

        user_obj = User.objects.get(pk=request.user.id)

        # Save Dataset record
        dataset = Dataset()
        dataset.dataset_name = dataset_name
        dataset.data = json_data
        dataset.document = uploaded_file_url
        dataset.user_id = user_obj
        dataset.process_id = process_obj
        dataset.dataset_id = d_id
        dataset.save()

        # Save column metadata (replaces MongoDB headersData)
        for col_name, col_type in type_map.items():
            ColumnMeta.objects.create(
                dataset=dataset,
                column_name=col_name,
                data_type=col_type,
            )

        # Save Dataset_List record
        form1 = Dataset_List()
        form1.d_id = dataset
        form1.u_id = user_obj
        form1.p_id = process_obj
        form1.save()

        return JsonResponse({
            'fileData': dataInCsv,
            'datasetname': dataset_name,
            'typesArray': list(type_map.values()),
            'isDuplicate': False,
        })

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def changeDataType(request):
    """Update column data types for a dataset."""
    if request.method == 'POST':
        dataset_id = request.POST.get('dname', '')
        type_obj_str = request.POST.get('changedDataType', '{}')
        try:
            type_obj = ast.literal_eval(type_obj_str)
            dataset = Dataset.objects.get(dataset_id=dataset_id, user_id=request.user.id)
            for col_name, col_type in type_obj.items():
                ColumnMeta.objects.update_or_create(
                    dataset=dataset,
                    column_name=col_name,
                    defaults={'data_type': str(col_type)},
                )
            return HttpResponse('datatype has been saved', content_type='text/plain')
        except Exception as e:
            logger.error(f"Error updating data types: {e}")
            return HttpResponse('error in saving datatype', content_type='text/plain')
    return HttpResponse('invalid method', status=405)


def deleteDataset(request, dataset_name):
    """Delete a dataset and all related records from PostgreSQL."""
    try:
        dataset = Dataset.objects.get(dataset_name=dataset_name, user_id=request.user.id)
        # Cascade deletes will remove Dataset_List and ColumnMeta
        dataset.delete()
        return HttpResponse('Delete successful')
    except Dataset.DoesNotExist:
        return HttpResponse('Dataset does not exist')
    except Exception as e:
        logger.error(f"Error deleting dataset: {e}")
        return HttpResponse('Error during deletion')


def giveDatasetName(request):
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset_id', '')
        try:
            dataset = Dataset.objects.get(pk=dataset_id)
            return HttpResponse(dataset.dataset_name)
        except Dataset.DoesNotExist:
            return HttpResponse('Not found', status=404)


def mysqlconnect(request):
    """Connect to a MySQL database and return data as CSV."""
    if request.method == 'POST':
        try:
            import pymysql
            db_url = request.POST['dbUrl']
            db_user = request.POST['userName']
            db_name = request.POST['dbName']
            tb_name = request.POST['tbName']
            db_password = request.POST['password']
            db_port = int(request.POST['port'])

            conn = pymysql.connect(
                host=db_url, port=db_port, database=db_name,
                user=db_user, password=db_password
            )
            data = pd.read_sql_query(f'SELECT * FROM `{tb_name}`', conn)
            header_query = (
                "SELECT column_name, data_type FROM information_schema.columns "
                "WHERE TABLE_NAME = %s"
            )
            header_data = pd.read_sql_query(header_query, conn, params=[tb_name])
            conn.close()

            return JsonResponse({
                'csv': data.to_csv(index=False),
                'types': header_data.to_csv(index=False),
            })
        except Exception as e:
            logger.error(f"MySQL connect error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'POST required'}, status=405)
