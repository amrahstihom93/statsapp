from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.analytics.models import statistical, analytical, hypothetical
from apps.datasets.models import Dataset
from apps.processes.models import Process
from apps.accounts.models import ClientList

class AnalyticsTestCase(TestCase):
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
        self.dataset = Dataset.objects.create(
            dataset_name='Test Dataset',
            dataset_id='DS001',
            data=[{"col1": "val1", "col2": "val2"}],
            user_id=self.user,
            process_id=self.process
        )
        
        self.stat = statistical.objects.create(
            statistical_id='STAT001',
            statistical_name='Test Stat',
            statistical_method='Mean',
            statistical_calculated_value={"mean": 10},
            user_id=self.user,
            dataset_id=self.dataset,
            parameters={"col": "col1"},
            test='true'
        )

    def test_statistical_creation(self):
        self.assertEqual(statistical.objects.count(), 1)
        stat = statistical.objects.get(statistical_id='STAT001')
        self.assertEqual(stat.statistical_name, 'Test Stat')
        self.assertEqual(stat.statistical_calculated_value, {"mean": 10})
