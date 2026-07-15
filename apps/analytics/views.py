"""
statistical/views.py
Refactored to remove MongoDB dependency.
All data is fetched from Dataset.data (JSONField in PostgreSQL).
"""
import logging
import json
import datetime
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.datasets.models import Dataset
from .models import statistical, analytical, hypothetical
from django.contrib.auth.models import User
import statistics as stats_module
from statistics import mode
import scipy.stats as scipy_stats
from scipy.stats import kurtosis, shapiro, normaltest, anderson, pearsonr, spearmanr, kendalltau
from scipy.stats import ttest_1samp, ttest_ind, ttest_rel, chi2_contingency, f_oneway
from scipy.stats import mannwhitneyu, wilcoxon, kruskal, friedmanchisquare
import numpy as np

logger = logging.getLogger(__name__)


def _get_column_data(dataset_id, column_name, user_id):
    """
    Fetch a specific column from a dataset stored in PostgreSQL JSONField.
    Returns a list of float values.
    """
    try:
        dataset = Dataset.objects.get(dataset_id=dataset_id, user_id=user_id)
        df = pd.DataFrame(dataset.data)
        if column_name not in df.columns:
            return []
        return pd.to_numeric(df[column_name], errors='coerce').dropna().tolist()
    except Dataset.DoesNotExist:
        logger.error(f"Dataset {dataset_id} not found for user {user_id}")
        return []
    except Exception as e:
        logger.error(f"Error fetching column data: {e}")
        return []


# ─────────────────────────────────────────────────────────────
# SAVE FUNCTIONS
# ─────────────────────────────────────────────────────────────

def saveAnalytics(request):
    if request.method == 'POST':
        try:
            v = analytical()
            v.analytical_name = request.POST['analytical_name']
            v.dataset_id = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
            v.user_id = User.objects.get(pk=request.user.id)
            v.analytical_id = 'sid' + request.POST['analytical_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            v.analytical_method = request.POST['selectedmethod']
            v.analytical_calculated_value = request.POST['analytical_calculated_value']
            v.parameters = request.POST['fieldData']
            v.save()
            return HttpResponse('saved successfully')
        except Exception as e:
            logger.error(f"saveAnalytics error: {e}")
    return HttpResponse('error while saving analytical summary')


def saveStatistics(request):
    if request.method == 'POST':
        try:
            v = statistical()
            v.statistical_name = request.POST['statistical_name']
            v.dataset_id = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
            v.user_id = User.objects.get(pk=request.user.id)
            v.statistical_id = 'sid' + request.POST['statistical_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            v.statistical_method = request.POST['selectedmethod']
            v.statistical_calculated_value = request.POST['statistical_calculated_value']
            v.parameters = request.POST['fieldData']
            v.save()
            return HttpResponse('saved successfully')
        except Exception as e:
            logger.error(f"saveStatistics error: {e}")
    return HttpResponse('error while saving statistical summary')


def saveHypothesis(request):
    if request.method == 'POST':
        try:
            v = hypothetical()
            v.hypothetical_name = request.POST['hypothetical_name']
            v.user_id = User.objects.get(pk=request.user.id)
            v.dataset_id = Dataset.objects.get(dataset_id=request.POST['dataset_id'])
            v.hypothetical_method = request.POST['hypothetical_method']
            v.hypothetical_id = 'hid' + request.POST['hypothetical_name'] + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            v.hypothetical_calculated_value = request.POST['hypothetical_calculated_value']
            v.parameters = request.POST.get('fieldData', '{}')
            v.save()
            return HttpResponse('saved successfully')
        except Exception as e:
            logger.error(f"saveHypothesis error: {e}")
    return HttpResponse('error while saving hypothetical summary')


# ─────────────────────────────────────────────────────────────
# LIST FUNCTIONS
# ─────────────────────────────────────────────────────────────

def getStatisticalList(request):
    try:
        result = statistical.objects.filter(user_id=request.user.id).values()
        return JsonResponse(list(result), safe=False)
    except Exception as e:
        logger.error(f"getStatisticalList error: {e}")
        return HttpResponse('error', status=500)


def getAnalyticalList(request):
    try:
        result = analytical.objects.filter(user_id=request.user.id).values()
        return JsonResponse(list(result), safe=False)
    except Exception as e:
        logger.error(f"getAnalyticalList error: {e}")
        return HttpResponse('error', status=500)


def hypoList(request):
    try:
        result = hypothetical.objects.filter(user_id=request.user.id).values()
        return JsonResponse(list(result), safe=False)
    except Exception as e:
        logger.error(f"hypoList error: {e}")
        return HttpResponse('error', status=500)


# ─────────────────────────────────────────────────────────────
# DELETE FUNCTIONS
# ─────────────────────────────────────────────────────────────

def delStatistical(request, id):
    try:
        statistical.objects.get(pk=id, user_id=request.user.id).delete()
        return HttpResponse('delete successful')
    except statistical.DoesNotExist:
        return HttpResponse('not found', status=404)


def delAnalytical(request, id):
    try:
        analytical.objects.get(pk=id, user_id=request.user.id).delete()
        return HttpResponse('delete successful')
    except analytical.DoesNotExist:
        return HttpResponse('not found', status=404)


# ─────────────────────────────────────────────────────────────
# CALCULATE STATISTICS (Descriptive)
# ─────────────────────────────────────────────────────────────

def calculateStatistics(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    dataset_id = request.POST.get('dataset_id', '')
    column = request.POST.get('selecteddatacol', '')
    selected_method = request.POST.get('selectedmethod', '')

    data = _get_column_data(dataset_id, column, request.user.id)
    if not data:
        return JsonResponse({'error': 'No data found for column'}, status=400)

    result = {}
    try:
        if selected_method == 'Descriptive Statistics':
            result = {
                'count': len(data),
                'mean': round(float(np.mean(data)), 4),
                'median': round(float(np.median(data)), 4),
                'mode': round(float(stats_module.mode(data)), 4) if len(set(data)) < len(data) else 'N/A',
                'std': round(float(np.std(data, ddof=1)), 4),
                'variance': round(float(np.var(data, ddof=1)), 4),
                'min': round(float(np.min(data)), 4),
                'max': round(float(np.max(data)), 4),
                'range': round(float(np.max(data) - np.min(data)), 4),
                'skewness': round(float(scipy_stats.skew(data)), 4),
                'kurtosis': round(float(kurtosis(data)), 4),
                'q1': round(float(np.percentile(data, 25)), 4),
                'q3': round(float(np.percentile(data, 75)), 4),
                'iqr': round(float(np.percentile(data, 75) - np.percentile(data, 25)), 4),
            }
        else:
            result = {'error': f'Unknown method: {selected_method}'}
    except Exception as e:
        logger.error(f"calculateStatistics error: {e}")
        result = {'error': str(e)}

    return JsonResponse({'summary': result, 'selectedmethod': selected_method})


# ─────────────────────────────────────────────────────────────
# CALCULATE ANALYTICS (Normality / Parametric / Non-Parametric)
# ─────────────────────────────────────────────────────────────

def calculateAnalytics(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    dataset_id = request.POST.get('dataset_id', '')
    column = request.POST.get('selecteddatacol', '')
    selected_method = request.POST.get('selectedmethod', '')

    data = _get_column_data(dataset_id, column, request.user.id)
    if not data:
        return JsonResponse({'error': 'No data found for column'}, status=400)

    result = {}
    try:
        if selected_method == 'Shapiro-Wilk Test':
            stat, p = shapiro(data)
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Probably Gaussian' if p > 0.05 else 'Probably not Gaussian',
            }

        elif selected_method == "D'Agostino's K^2 Test":
            stat, p = normaltest(data)
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Probably Gaussian' if p > 0.05 else 'Probably not Gaussian',
            }

        elif selected_method == 'Anderson-Darling Test':
            res = anderson(data)
            result = {
                'stat': round(float(res.statistic), 4),
                'critical_values': list(res.critical_values),
                'significance_levels': list(res.significance_level),
            }

        elif selected_method == "Pearson's Correlation Coefficient":
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            min_len = min(len(data), len(data2))
            stat, p = pearsonr(data[:min_len], data2[:min_len])
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Probably independent' if p > 0.05 else 'Probably dependent',
            }

        elif selected_method == "Spearman's Rank Correlation":
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            min_len = min(len(data), len(data2))
            stat, p = spearmanr(data[:min_len], data2[:min_len])
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Probably independent' if p > 0.05 else 'Probably dependent',
            }

        elif selected_method == "Kendall's Rank Correlation":
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            min_len = min(len(data), len(data2))
            stat, p = kendalltau(data[:min_len], data2[:min_len])
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Probably independent' if p > 0.05 else 'Probably dependent',
            }

        elif selected_method == 'Student t-test (one sample)':
            popmean = float(request.POST.get('popmean', 0))
            stat, p = ttest_1samp(data, popmean)
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
            }

        elif selected_method == 'Student t-test (two sample)':
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            stat, p = ttest_ind(data, data2)
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
            }

        elif selected_method == 'Chi-Square Test':
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            chi2, p, dof, expected = chi2_contingency([data, data2])
            result = {
                'chi2': round(float(chi2), 4),
                'p': round(float(p), 4),
                'dof': int(dof),
                'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
            }

        elif selected_method == 'One-way ANOVA':
            groups_raw = request.POST.get('groups', '[]')
            groups = json.loads(groups_raw)
            group_data = [_get_column_data(dataset_id, g, request.user.id) for g in groups]
            group_data = [g for g in group_data if g]
            if len(group_data) >= 2:
                stat, p = f_oneway(*group_data)
                result = {
                    'stat': round(float(stat), 4),
                    'p': round(float(p), 4),
                    'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
                }
            else:
                result = {'error': 'Need at least 2 groups for ANOVA'}

        elif selected_method == 'Mann-Whitney U Test':
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            stat, p = mannwhitneyu(data, data2, alternative='two-sided')
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
            }

        elif selected_method == 'Wilcoxon Signed-Rank Test':
            column2 = request.POST.get('selecteddatacol2', '')
            dataset_id2 = request.POST.get('dataset_id2', dataset_id)
            data2 = _get_column_data(dataset_id2, column2, request.user.id)
            min_len = min(len(data), len(data2))
            stat, p = wilcoxon(data[:min_len], data2[:min_len])
            result = {
                'stat': round(float(stat), 4),
                'p': round(float(p), 4),
                'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
            }

        elif selected_method == 'Kruskal-Wallis Test':
            groups_raw = request.POST.get('groups', '[]')
            groups = json.loads(groups_raw)
            group_data = [_get_column_data(dataset_id, g, request.user.id) for g in groups]
            group_data = [g for g in group_data if g]
            if len(group_data) >= 2:
                stat, p = kruskal(*group_data)
                result = {
                    'stat': round(float(stat), 4),
                    'p': round(float(p), 4),
                    'conclusion': 'Fail to reject H0' if p > 0.05 else 'Reject H0',
                }
            else:
                result = {'error': 'Need at least 2 groups'}

        else:
            result = {'error': f'Unknown method: {selected_method}'}

    except Exception as e:
        logger.error(f"calculateAnalytics error ({selected_method}): {e}")
        result = {'error': str(e)}

    return JsonResponse({'summary': result, 'selectedmethod': selected_method})


# ─────────────────────────────────────────────────────────────
# CALCULATE HYPOTHESIS
# ─────────────────────────────────────────────────────────────

def calculateHypothesis(request):
    """Delegates to calculateAnalytics — hypothesis tests use the same logic."""
    return calculateAnalytics(request)
