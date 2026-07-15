import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

logger = logging.getLogger(__name__)


def processmap(request):
    logger.info("Rendering process map")
    return render(request, 'processmap/pmap.html')


def processmapopen(request):
    logger.info("Opening process map")
    return render(request, 'processmap/open.html')


def processmapsave(request):
    """Save process map data — returns JSON confirmation."""
    if request.method == 'POST':
        logger.info("Saving process map")
        # Process map data is handled client-side (canvas state)
        # This endpoint confirms the save action
        return JsonResponse({'status': 'ok', 'message': 'Process map saved'})
    return HttpResponse('POST required', status=405)
