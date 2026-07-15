"""
apps/analytics/api_views.py
JSON REST endpoints for analytics summaries used by the React frontend.
"""
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import statistical, analytical, hypothetical
from apps.machinelearning.models import mlearn
from apps.datasets.models import Dataset


@login_required
def stats_list_view(request):
    """GET /api/v1/analytics/stats/ — all saved statistical analyses."""
    qs = statistical.objects.filter(user_id=request.user).values(
        'id', 'statistical_name', 'statistical_method',
        'statistical_calculated_value', 'parameters'
    )
    return JsonResponse(list(qs), safe=False)


@login_required
def analytics_list_view(request):
    """GET /api/v1/analytics/analytical/ — all saved analytical analyses."""
    qs = analytical.objects.filter(user_id=request.user).values(
        'id', 'analytical_name', 'analytical_method',
        'analytical_calculated_value', 'parameters'
    )
    return JsonResponse(list(qs), safe=False)


@login_required
def ml_models_view(request):
    """GET /api/v1/analytics/models/ — all saved ML models for the user."""
    qs = mlearn.objects.filter(user_id=request.user).values(
        'id', 'mlearn_name', 'mlearn_id', 'parameters'
    )
    return JsonResponse(list(qs), safe=False)


@login_required
def dashboard_summary_view(request):
    """GET /api/v1/analytics/summary/ — quick KPI counts for the dashboard."""
    dataset_count = Dataset.objects.filter(user_id=request.user).count()
    stats_count = statistical.objects.filter(user_id=request.user).count()
    ml_count = mlearn.objects.filter(user_id=request.user).count()
    return JsonResponse({
        'dataset_count': dataset_count,
        'stats_count': stats_count,
        'ml_model_count': ml_count,
    })
