"""
apps/accounts/api_views.py
JSON REST endpoints for the React frontend (session + CSRF auth).
"""
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST
from .models import Profile, ClientList


# ── CSRF bootstrap ────────────────────────────────────────────────────────────

@ensure_csrf_cookie
def csrf_token_view(request):
    """GET this endpoint first to receive the CSRF cookie."""
    return JsonResponse({'detail': 'CSRF cookie set'})


# ── Auth ──────────────────────────────────────────────────────────────────────

@ensure_csrf_cookie
def me(request):
    """Return current session user profile as JSON."""
    if not request.user.is_authenticated:
        return JsonResponse({'authenticated': False}, status=401)
    user = request.user
    try:
        profile = user.profile
        client_data = None
        if profile.client:
            client_data = {
                'client_id': profile.client.client_id,
                'company_name': profile.client.company_name,
                'email_id': profile.client.email_id,
            }
        return JsonResponse({
            'authenticated': True,
            'user': str(profile.uuid),
            'username': user.username,
            'email': user.email,
            'phone_number': str(profile.phone_number) if profile.phone_number else '',
            'email_confirmed': profile.email_confirmed,
            'is_admin': profile.is_admin,
            'has_seen_tour': profile.has_seen_tour,
            'client': client_data,
        })
    except Profile.DoesNotExist:
        return JsonResponse({'authenticated': True, 'user': str(user.id), 'email': user.email})


@csrf_exempt
def login_view(request):
    """POST {username, password} — returns profile JSON on success."""
    if request.method == 'OPTIONS':
        return JsonResponse({})
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')
    except (json.JSONDecodeError, AttributeError):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    if not user.is_active:
        return JsonResponse({'error': 'Account not activated. Check your email.'}, status=403)
    login(request, user)
    return me(request)


@require_POST
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': 'Logged out'})


@login_required
@require_POST
def complete_tour_view(request):
    profile = request.user.profile
    profile.has_seen_tour = True
    profile.save()
    return JsonResponse({'status': 'ok', 'has_seen_tour': True})


# ── Clients ───────────────────────────────────────────────────────────────────

@login_required
def clients_view(request):
    if request.method == 'GET':
        qs = ClientList.objects.all().values('client_id', 'company_name', 'email_id')
        return JsonResponse(list(qs), safe=False)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        company_name = data.get('company_name', '').strip()
        email_id = data.get('email_id', '').strip()
        if not company_name or not email_id:
            return JsonResponse({'error': 'company_name and email_id are required'}, status=400)
        import datetime
        client_id = 'CID' + company_name + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        client = ClientList.objects.create(
            client_id=client_id,
            company_name=company_name,
            email_id=email_id,
        )
        return JsonResponse({
            'client_id': client.client_id,
            'company_name': client.company_name,
            'email_id': client.email_id,
        }, status=201)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ── Users / admin ─────────────────────────────────────────────────────────────

@login_required
def users_view(request):
    """Admin-only: list all users with their profiles."""
    if not request.user.profile.is_admin:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    result = []
    for user in User.objects.select_related('profile__client').all():
        try:
            p = user.profile
            client_data = None
            if p.client:
                client_data = {
                    'client_id': p.client.client_id,
                    'company_name': p.client.company_name,
                    'email_id': p.client.email_id,
                }
            result.append({
                'user': str(p.uuid),
                'django_id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': str(p.phone_number) if p.phone_number else '',
                'email_confirmed': p.email_confirmed,
                'is_admin': p.is_admin,
                'has_seen_tour': p.has_seen_tour,
                'client': client_data,
            })
        except Profile.DoesNotExist:
            pass
    return JsonResponse(result, safe=False)


@login_required
@require_POST
def assign_client_view(request, user_id):
    """POST {client_id} — assign a client to any user (admin only)."""
    if not request.user.profile.is_admin:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    client_id = data.get('client_id', '').strip()
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if not client_id:
        target_user.profile.client = None
    else:
        try:
            client = ClientList.objects.get(client_id=client_id)
            target_user.profile.client = client
        except ClientList.DoesNotExist:
            return JsonResponse({'error': 'Client not found'}, status=404)

    target_user.profile.save()
    return JsonResponse({'status': 'ok'})
