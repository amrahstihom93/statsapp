"""
Management command to bootstrap a test admin user for local development.
"""
import os
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import Profile, ClientList

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser('admin', 'admin@local.dev', 'admin123')
    client, _ = ClientList.objects.get_or_create(
        client_id='CIDTestCompany',
        defaults={
            'company_name': 'Test Company',
            'email_id': 'admin@local.dev',
        }
    )
    user.profile.client = client
    user.profile.email_confirmed = True
    user.profile.is_admin = True
    user.is_active = True
    user.profile.save()
    user.save()
    print('✅ Superuser created: admin / admin123')
else:
    print('ℹ️  Admin user already exists')

# Also seed a root process if none exists
from apps.processes.models import Process, Process_List
import datetime
admin = User.objects.get(username='admin')
client = admin.profile.client

if not Process.objects.filter(user_id=admin).exists():
    process = Process.objects.create(
        process_id='PIDroot' + datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        process_name='root',
        parent_p_id='PID00000000000000',
        client_id=client,
        user_id=admin,
    )
    Process_List.objects.create(process_id=process, user_id=admin)
    print('✅ Root process created')
else:
    print('ℹ️  Root process already exists')
