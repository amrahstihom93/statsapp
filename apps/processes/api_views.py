"""
apps/processes/api_views.py
JSON REST endpoints for process management used by the React frontend.
"""
import json, datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Process, Process_List


def _serialize_process(p):
    return {
        'process_id': p.process_id,
        'process_name': p.process_name,
        'parent_p_id': p.parent_p_id,
        'client_id': p.client_id.client_id if p.client_id else None,
    }


@login_required
def processes_view(request):
    """GET /api/v1/processes/ — list all processes for the current user.
       POST — create a new process."""
    if request.method == 'GET':
        qs = Process.objects.filter(user_id=request.user)
        return JsonResponse([_serialize_process(p) for p in qs], safe=False)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST

        process_name = data.get('process_name', '').strip()
        parent_process = data.get('parent_process', 'root')
        if not process_name:
            return JsonResponse({'error': 'process_name is required'}, status=400)

        process_id = 'PID' + process_name + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        if parent_process == 'root':
            parent_p_id = 'PID' + 'root' + '00000000000000'
        else:
            parent_p_id = parent_process

        client = None
        try:
            client = request.user.profile.client
        except Exception:
            pass

        p = Process.objects.create(
            process_id=process_id,
            process_name=process_name,
            parent_p_id=parent_p_id,
            user_id=request.user,
            client_id=client,
        )
        Process_List.objects.create(process_id=p, user_id=request.user)
        return JsonResponse(_serialize_process(p), status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
