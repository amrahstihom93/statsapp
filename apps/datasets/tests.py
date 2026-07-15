from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.datasets.models import Dataset, ColumnMeta, Dataset_List
from apps.processes.models import Process
from apps.accounts.models import ClientList

class DatasetsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        
        self.client_list = ClientList.objects.create(
            company_name='Test Company',
            client_id='TC001',
            email_id='test@company.com'
        )
        self.process = Process.objects.create(
            process_name='Test Process',
            process_id='PR001',
            parent_p_id='P_PR001',
            client_id=self.client_list
        )
        
        self.dataset = Dataset.objects.create(
            dataset_name='Test Dataset',
            dataset_id='DS001',
            data=[{"col1": "val1", "col2": "val2"}],
            user_id=self.user,
            process_id=self.process
        )
        
        ColumnMeta.objects.create(
            dataset=self.dataset,
            column_name='col1',
            data_type='string'
        )
        ColumnMeta.objects.create(
            dataset=self.dataset,
            column_name='col2',
            data_type='string'
        )
        
        Dataset_List.objects.create(
            d_id=self.dataset,
            u_id=self.user,
            p_id=self.process
        )

    def test_dataset_creation(self):
        self.assertEqual(Dataset.objects.count(), 1)
        self.assertEqual(Dataset.objects.get(dataset_id='DS001').dataset_name, 'Test Dataset')

    def test_column_meta_creation(self):
        self.assertEqual(ColumnMeta.objects.count(), 2)
        cols = ColumnMeta.objects.filter(dataset=self.dataset)
        col_names = [c.column_name for c in cols]
        self.assertIn('col1', col_names)
        self.assertIn('col2', col_names)
