import logging
import json
import datetime
import numpy as np
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.datasets.models import Dataset, ColumnMeta
from .models import visualization
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def chart(request):
    return render(request, 'analytics/chart.html')


def _get_dataset_df(dataset_id):
    """Load a dataset's row data into a pandas DataFrame."""
    try:
        dataset = Dataset.objects.get(dataset_id=dataset_id)
        data = dataset.data  # list of dicts stored in JSONField
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
    except Dataset.DoesNotExist:
        return pd.DataFrame()


def makechart(request, graph_type, dataset_name):
    try:
        dataset = Dataset.objects.get(dataset_name=dataset_name, user_id=request.user.id)
        columns = ColumnMeta.objects.filter(dataset=dataset).values_list('column_name', flat=True)
        return render(request, 'analytics/makechart.html', {
            'dataset_name': dataset_name,
            'fields': list(columns),
        })
    except Dataset.DoesNotExist:
        return HttpResponse('Dataset not found', status=404)


def get_data(request, graph_type, dataset_name):
    labels = []
    default_items = []
    if request.method == 'POST':
        x = request.POST.get('x_axis_value', '')
        y = request.POST.get('y_axis_value', '')
        try:
            dataset = Dataset.objects.get(dataset_name=dataset_name, user_id=request.user.id)
            df = pd.DataFrame(dataset.data)
            if x in df.columns and y in df.columns:
                labels = df[x].tolist()
                default_items = df[y].tolist()
        except Exception as e:
            logger.error(f"Chart data error: {e}")
    return JsonResponse({"labels": labels, "default": default_items})


@csrf_exempt
def visualization_data(request, dataset_name):
    labels = []
    default_items = []
    x = request.POST.get('x_value', '')
    y = request.POST.get('y_value', '')
    try:
        dataset = Dataset.objects.get(dataset_name=dataset_name, user_id=request.user.id)
        df = pd.DataFrame(dataset.data)
        if x in df.columns and y in df.columns:
            labels = df[x].tolist()
            default_items = df[y].tolist()
    except Exception as e:
        logger.error(f"Visualization data error: {e}")
    return JsonResponse({"labels": labels, "default": default_items})


def get_visualization(request, dataset_name):
    try:
        dataset = Dataset.objects.get(dataset_name=dataset_name, user_id=request.user.id)
        columns = ColumnMeta.objects.filter(dataset=dataset).values_list('column_name', flat=True)
        return render(request, 'analytics/visualization.html', {
            'dataset_name': dataset_name,
            'fields': list(columns),
        })
    except Dataset.DoesNotExist:
        return HttpResponse('Dataset not found', status=404)


def getDataset(request):
    try:
        datasets = Dataset.objects.filter(user_id=request.user.id).values(
            'dataset_id', 'dataset_name', 'uploaded_at', 'process_id'
        )
        return JsonResponse(list(datasets), safe=False)
    except Exception as e:
        logger.error(f"getDataset error: {e}")
        return HttpResponse('Error retrieving datasets', status=500)


def getGraphFields(request):
    dataset_id = request.POST.get('dName', '')
    try:
        dataset = Dataset.objects.get(dataset_id=dataset_id, user_id=request.user.id)
        columns = ColumnMeta.objects.filter(dataset=dataset).values_list('column_name', flat=True)
        return JsonResponse(list(columns), safe=False)
    except Dataset.DoesNotExist:
        return JsonResponse([], safe=False)
    except Exception as e:
        logger.error(f"getGraphFields error: {e}")
        return JsonResponse([], safe=False)


def getGraphData(request):
    labels = []
    default_items = []
    dataset_name = request.POST.get('dtName', '')
    x = request.POST.get('x_value', '')
    y = request.POST.get('y_value', '')
    try:
        dataset = Dataset.objects.get(dataset_name=dataset_name, user_id=request.user.id)
        df = pd.DataFrame(dataset.data)
        if x in df.columns and y in df.columns:
            labels = df[x].tolist()
            default_items = df[y].tolist()
    except Exception as e:
        logger.error(f"getGraphData error: {e}")
    return JsonResponse({"labels": labels, "defaultData": default_items})


def saveVisualization(request):
    if request.method == 'POST':
        try:
            v = visualization()
            v.visualization_name = request.POST['visualization_name']
            v.type = request.POST['graphType']
            v.parameters = json.loads(request.POST['data'])
            v.dataset_id = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
            v.user_id = User.objects.get(pk=request.user.id)
            v.visualization_id = (
                'vid' + request.POST['visualization_name']
                + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            )
            v.save()
            return HttpResponse('saved successfully')
        except Exception as e:
            logger.error(f"saveVisualization error: {e}")
            return HttpResponse('error', status=500)
    return HttpResponse('error', status=405)


def getVisualizationList(request):
    try:
        vis_list = visualization.objects.filter(user_id=request.user.id).values()
        return JsonResponse(list(vis_list), safe=False)
    except Exception as e:
        logger.error(f"getVisualizationList error: {e}")
        return HttpResponse('error', status=500)


def delVisualization(request, id):
    try:
        visualization.objects.get(pk=id, user_id=request.user.id).delete()
        return HttpResponse('delete successful')
    except visualization.DoesNotExist:
        return HttpResponse('delete unsuccessful', status=404)


def editVisualisation(request):
    if request.method == 'POST':
        try:
            v = visualization.objects.get(pk=request.POST['visualization_id'], user_id=request.user.id)
            name = request.POST.get('visualization_name', '')
            if name:
                v.visualization_name = name
            v.parameters = json.loads(request.POST['data'])
            v.save()
            return HttpResponse('saved successfully')
        except Exception as e:
            logger.error(f"editVisualisation error: {e}")
            return HttpResponse('something went wrong', status=500)
    return HttpResponse('error', status=405)


def getSubgroup(request):
    """Return SPC subgroup constants table."""
    data = {
        'Subgroup': list(range(2, 26)),
        'A2': [1.880, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337,
               0.308, 0.285, 0.266, 0.249, 0.235, 0.223, 0.212, 0.203,
               0.194, 0.187, 0.180, 0.173, 0.167, 0.162, 0.157, 0.153],
        'd2': [1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970,
               3.078, 3.173, 3.258, 3.336, 3.407, 3.472, 3.532, 3.588,
               3.640, 3.689, 3.735, 3.778, 3.819, 3.858, 3.895, 3.931],
        'D3': [0.000, 0.000, 0.000, 0.000, 0.000, 0.076, 0.136, 0.184,
               0.223, 0.256, 0.283, 0.307, 0.328, 0.347, 0.363, 0.378,
               0.391, 0.403, 0.415, 0.425, 0.434, 0.443, 0.451, 0.459],
        'D4': [3.268, 2.574, 2.282, 2.114, 2.004, 1.924, 1.864, 1.816,
               1.777, 1.744, 1.717, 1.693, 1.672, 1.653, 1.637, 1.622,
               1.608, 1.597, 1.585, 1.575, 1.566, 1.557, 1.548, 1.541],
    }
    df = pd.DataFrame(data)
    return JsonResponse(df.to_json(orient='split'), safe=False)
