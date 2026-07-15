from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.processes.models import Process, Process_List
from apps.accounts.models import ClientList

class ProcessesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        
        self.client_list = ClientList.objects.create(
            company_name='Test Company',
            client_id='TC001',
            email_id='test@company.com'
        )
        
        self.process = Process.objects.create(
            process_id='PR001',
            process_name='Test Process',
            parent_p_id='P_PR001',
            client_id=self.client_list,
            user_id=self.user
        )
        
        Process_List.objects.create(
            process_id=self.process,
            user_id=self.user
        )

    def test_process_creation(self):
        self.assertEqual(Process.objects.count(), 1)
        process = Process.objects.get(process_id='PR001')
        self.assertEqual(process.process_name, 'Test Process')
        self.assertEqual(process.client_id.company_name, 'Test Company')

    def test_process_list_creation(self):
        self.assertEqual(Process_List.objects.count(), 1)
        pl = Process_List.objects.get(process_id=self.process)
        self.assertEqual(pl.user_id.username, 'testuser')
