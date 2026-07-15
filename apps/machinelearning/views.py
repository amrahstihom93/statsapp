"""
mlearn/views.py
Refactored to remove MongoDB dependency and fix global state race condition.
ML models are stored in the database (mlearn model) and as pkl files in media/.
"""
import logging
import json
import datetime
import os
import pickle
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for server use
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from apps.datasets.models import Dataset
from django.contrib.auth.models import User
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from json import JSONEncoder
import statsmodels.api as sm
from .models import mlearn as MLModel

logger = logging.getLogger(__name__)


class NumpyEncoder(JSONEncoder):
    """JSON encoder that handles numpy arrays and scalars."""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        return super().default(obj)


def mlearn(request):
    return render(request, 'datasets/datasetlist.html', {'STATIC_URL': settings.STATIC_URL})


def _get_dataset_column(dataset_id, column_name):
    """Load a column from a dataset stored in PostgreSQL JSONField."""
    try:
        dataset = Dataset.objects.get(dataset_id=dataset_id)
        df = pd.DataFrame(dataset.data)
        if column_name not in df.columns:
            return None, f"Column '{column_name}' not found in dataset"
        return pd.to_numeric(df[column_name], errors='coerce').dropna(), None
    except Dataset.DoesNotExist:
        return None, "Dataset not found"
    except Exception as e:
        return None, str(e)


@csrf_exempt
def calcsregression(request):
    """Simple linear regression calculation."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        training_size = int(request.POST.get('training_size', 80))
        random_state = int(request.POST.get('random_state', 42))
        fit_intercept_str = request.POST.get('fit_intercept', 'True').strip('"').lower()
        fit_intercept = fit_intercept_str in ('true', '1', 'yes')
        dataset_id = request.POST.get('dataset_id', '')
        dvar = request.POST.get('dvar', '')   # dependent variable (y)
        idvar = request.POST.get('idvar', '') # independent variable (x)

        # Load data from PostgreSQL
        dataset = Dataset.objects.get(dataset_id=dataset_id)
        df = pd.DataFrame(dataset.data)

        if dvar not in df.columns or idvar not in df.columns:
            return JsonResponse({'error': f'Columns not found: {dvar}, {idvar}'}, status=400)

        x = pd.to_numeric(df[idvar], errors='coerce').dropna().values.reshape(-1, 1)
        y = pd.to_numeric(df[dvar], errors='coerce').dropna().values.reshape(-1, 1)

        # Align lengths
        min_len = min(len(x), len(y))
        x, y = x[:min_len], y[:min_len]

        test_size = 1 - (training_size / 100)
        if random_state == 0:
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
        else:
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)

        # Fit model
        regressor = LinearRegression(fit_intercept=fit_intercept)
        regressor.fit(x_train, y_train)

        # Score
        y_pred = regressor.predict(x_test)
        result_score = r2_score(y_test, y_pred)

        # OLS summary
        x_test_f = x_test.astype(float)
        y_test_f = y_test.astype(float)
        ols_model = sm.OLS(y_test_f, x_test_f).fit()

        rs = float(ols_model.rsquared)
        rad = float(ols_model.rsquared_adj)
        stderoe = float(np.mean(ols_model.bse)) * 100
        pvalue = float(np.mean(ols_model.pvalues))
        tvalue = float(np.mean(ols_model.tvalues))
        fvalue = float(ols_model.fvalue)

        xtrain_pred = regressor.predict(x_train)

        # Store the model as session data (NOT global state) for potential save
        model_data = {
            'result_score': f"{100 * result_score:.2f} %",
            'rsquared': f"{rs:.5}",
            'radjective': f"{rad:.5}",
            'err_of_estimate': f"{stderoe:.5}",
            'fvalue': f"{fvalue:.5}",
            'pvalue': f"{pvalue:.3f}",
            'tvalue': f"{tvalue:.5}",
            'xtrain': json.dumps({'xtrain_array': x_train.tolist()}, cls=NumpyEncoder),
            'xtrain_pred': json.dumps({'conv_pred_array': xtrain_pred.tolist()}, cls=NumpyEncoder),
            'xtest': json.dumps({'xtest_array': x_test.tolist()}, cls=NumpyEncoder),
            'ytest': json.dumps({'ytest_array': y_test.tolist()}, cls=NumpyEncoder),
        }

        # Save model pickle to media/models/
        model_dir = os.path.join(settings.MEDIA_ROOT, 'models')
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, f'linear_model_temp_{request.user.id}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(regressor, f)

        # Store model data in session for save operation
        request.session['last_ml_model_path'] = model_path
        request.session['last_ml_model_data'] = model_data

        return JsonResponse({'summary': model_data}, encoder=NumpyEncoder)

    except Dataset.DoesNotExist:
        return JsonResponse({'error': 'Dataset not found'}, status=404)
    except Exception as e:
        logger.error(f"calcsregression error: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def saveMLmodel(request):
    """Save the most recent ML model results to the database."""
    if request.method != 'POST':
        return HttpResponse('POST required', status=405)

    try:
        model_name = request.POST.get('model_name', 'model')
        model_data = request.session.get('last_ml_model_data', {})
        model_path = request.session.get('last_ml_model_path', '')

        if not model_path or not os.path.exists(model_path):
            return HttpResponse('No model to save — run regression first', status=400)

        # Rename model file to the user-given name
        model_dir = os.path.dirname(model_path)
        final_path = os.path.join(model_dir, f'{model_name}.pkl')
        os.rename(model_path, final_path)

        # Save to database
        v = MLModel()
        v.mlearn_name = model_name
        v.user_id = User.objects.get(pk=request.user.id)
        v.mlearn_id = f'ml_{model_name}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
        v.parameters = model_data
        v.save()

        # Clear session
        request.session.pop('last_ml_model_path', None)
        request.session.pop('last_ml_model_data', None)

        return HttpResponse('saved successfully')

    except Exception as e:
        logger.error(f"saveMLmodel error: {e}", exc_info=True)
        return HttpResponse(f'Error: {e}', status=500)


@csrf_exempt
def multiregression(request):
    """Multiple linear regression calculation."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        training_size = int(request.POST.get('training_size', 80))
        random_state = int(request.POST.get('random_state', 42))
        dataset_id = request.POST.get('dataset_id', '')
        dvar = request.POST.get('dvar', '')             # dependent variable (y)
        idvar_str = request.POST.get('idvar', '')       # independent variables (x1,x2,...)

        idvars = [v.strip() for v in idvar_str.split(',') if v.strip()]

        dataset = Dataset.objects.get(dataset_id=dataset_id)
        df = pd.DataFrame(dataset.data)

        # Validate columns
        all_cols = [dvar] + idvars
        missing = [c for c in all_cols if c not in df.columns]
        if missing:
            return JsonResponse({'error': f'Columns not found: {missing}'}, status=400)

        y = pd.to_numeric(df[dvar], errors='coerce').fillna(0).values
        X = df[idvars].apply(pd.to_numeric, errors='coerce').fillna(0).values

        test_size = 1 - (training_size / 100)
        if random_state == 0:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        reg = LinearRegression()
        reg.fit(X_train, y_train)
        score = reg.score(X_test, y_test)

        X_sm = sm.add_constant(X.astype(float))
        ols_model = sm.OLS(y.astype(float), X_sm).fit()

        result = {
            'score': round(float(score), 5),
            'rsquared': round(float(ols_model.rsquared), 5),
            'radjective': round(float(ols_model.rsquared_adj), 5),
            'coefficients': reg.coef_.tolist(),
            'intercept': float(reg.intercept_),
            'fvalue': round(float(ols_model.fvalue), 5),
            'pvalue': json.loads(ols_model.pvalues.to_json()),
        }

        return JsonResponse({'summary': result})

    except Dataset.DoesNotExist:
        return JsonResponse({'error': 'Dataset not found'}, status=404)
    except Exception as e:
        logger.error(f"multiregression error: {e}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)


def mlist(request):
    """List all saved ML models for the current user."""
    try:
        ml_list = MLModel.objects.filter(user_id=request.user.id).values()
        return JsonResponse(list(ml_list), safe=False)
    except Exception as e:
        logger.error(f"mlist error: {e}")
        return HttpResponse('error', status=500)


def mldat(request):
    """Debug endpoint — list available ML models."""
    try:
        count = MLModel.objects.filter(user_id=request.user.id).count()
        return HttpResponse(f"You have {count} saved ML models.")
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)
