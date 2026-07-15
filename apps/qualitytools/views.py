"""
qtools/views.py
Refactored to remove MongoDB dependency.
FMEA data is stored in PostgreSQL via the fmea model's sheet_data JSONField.
"""
import logging
import json
import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from apps.processes.models import Process
from .models import fmea

logger = logging.getLogger(__name__)


def qtools(request):
    return render(request, 'qtools.html')


def opptracker(request):
    return render(request, 'opptrack.html')


def fmeaList(request):
    try:
        fmea_list = fmea.objects.filter(user_id=request.user.id).values(
            'id', 'fmea_name', 'fmea_sheetid', 'process_id'
        )
        return JsonResponse(list(fmea_list), safe=False)
    except Exception as e:
        logger.error(f"fmeaList error: {e}")
        return HttpResponse('error while getting FMEA list', status=500)


def saveFMEA(request):
    if request.method == 'POST':
        try:
            fmea_params_str = request.POST.get('fmeaparam', '[]')
            fmea_data = json.loads(fmea_params_str)

            v = fmea()
            v.fmea_name = request.POST.get('fmeaName', '')
            v.user_id = User.objects.get(pk=request.user.id)
            v.fmea_sheetid = 'fmea_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            v.sheet_data = fmea_data  # stored directly in PostgreSQL JSONField

            process_id = request.POST.get('process_id', '')
            if process_id:
                try:
                    v.process_id = Process.objects.get(pk=process_id)
                except Process.DoesNotExist:
                    logger.warning(f"Process {process_id} not found for FMEA save")

            v.save()
            return HttpResponse('saved successfully')
        except json.JSONDecodeError as e:
            logger.error(f"saveFMEA JSON error: {e}")
            return HttpResponse('invalid JSON data', status=400)
        except Exception as e:
            logger.error(f"saveFMEA error: {e}")
            return HttpResponse('error while saving FMEA sheet', status=500)
    return HttpResponse('POST required', status=405)
