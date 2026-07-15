"""
apps/datasets/api_views.py
JSON REST endpoints for dataset CRUD used by the React frontend.
"""
import json, datetime
import pandas as pd
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Dataset, Dataset_List, ColumnMeta
from apps.processes.models import Process


@login_required
def datasets_list_view(request):
    """GET /api/v1/datasets/ — list all datasets for the current user."""
    qs = Dataset.objects.filter(user_id=request.user).order_by('-uploaded_at')
    result = []
    for ds in qs:
        cols = list(ds.columns.values('column_name', 'data_type'))
        row_count = len(ds.data) if isinstance(ds.data, list) else 0
        result.append({
            'dataset_id': ds.dataset_id,
            'dataset_name': ds.dataset_name,
            'uploaded_at': ds.uploaded_at.isoformat(),
            'row_count': row_count,
            'col_count': len(cols),
            'columns': cols,
            'process_id': ds.process_id.process_id if ds.process_id else None,
        })
    return JsonResponse(result, safe=False)


@login_required
def dataset_preview_view(request, dataset_id):
    """GET /api/v1/datasets/<id>/preview/ — return first 10 rows."""
    try:
        ds = Dataset.objects.get(dataset_id=dataset_id, user_id=request.user)
    except Dataset.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    data = ds.data if isinstance(ds.data, list) else []
    cols = list(ds.columns.values_list('column_name', flat=True))
    return JsonResponse({
        'dataset_id': ds.dataset_id,
        'dataset_name': ds.dataset_name,
        'columns': cols,
        'preview': data[:10],
        'total_rows': len(data),
    })


@login_required
@csrf_exempt
def dataset_upload_view(request):
    """POST /api/v1/datasets/upload/ — upload a CSV or Excel file."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    dataset_name = request.POST.get('datasetName', '').strip()
    file_type = request.POST.get('fileType', 'csv')
    process_id_str = request.POST.get('process_id', '')
    csv_file = request.FILES.get('myfile')

    if not dataset_name:
        return JsonResponse({'error': 'datasetName is required'}, status=400)
    if csv_file is None:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    # Determine process — use user root process if not specified
    process_obj = None
    if process_id_str:
        try:
            process_obj = Process.objects.get(pk=process_id_str)
        except Process.DoesNotExist:
            pass
    if process_obj is None:
        process_obj = Process.objects.filter(
            user_id=request.user, parent_p_id='PID00000000000000'
        ).first()

    # Parse file
    try:
        if file_type in ('xls', 'xlsx'):
            df = pd.read_excel(csv_file)
        else:
            csv_file.seek(0)
            df = pd.read_csv(csv_file)
    except Exception as e:
        return JsonResponse({'error': f'Could not parse file: {e}'}, status=400)

    json_data = json.loads(df.to_json(orient='records'))
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

    d_id = 'DID' + dataset_name + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ds = Dataset.objects.create(
        dataset_name=dataset_name,
        dataset_id=d_id,
        data=json_data,
        user_id=request.user,
        process_id=process_obj,
    )
    for col_name, col_type in type_map.items():
        ColumnMeta.objects.create(dataset=ds, column_name=col_name, data_type=col_type)

    if process_obj:
        Dataset_List.objects.create(d_id=ds, u_id=request.user, p_id=process_obj)

    return JsonResponse({
        'dataset_id': ds.dataset_id,
        'dataset_name': ds.dataset_name,
        'row_count': len(json_data),
        'col_count': len(type_map),
    }, status=201)


@login_required
def dataset_delete_view(request, dataset_id):
    """DELETE /api/v1/datasets/<id>/delete/"""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'DELETE required'}, status=405)
    try:
        ds = Dataset.objects.get(dataset_id=dataset_id, user_id=request.user)
        ds.delete()
        return JsonResponse({'status': 'deleted'})
    except Dataset.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
