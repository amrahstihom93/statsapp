"""statsproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from statsapp import views

from mlearn import views as ml_views

#from statsapp.views import MyPDFView
from accounts import views as accounts_views
from upload import views as dataset_upload_views
from charts import views as chart_views
from process import views as process_views
from statistical import views as statistical_views

from django.contrib.auth import views as auth_views
#from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^test/$', views.hometest, name='main'),
	url(r'^makeCol/$', dataset_upload_views.makeCol, name='makeCol'),
	url(r'^signup/$', accounts_views.signup, name='signup'),
	#	url(r'^signup_success/$', accounts_views.signup_success, name='signup-success'),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	url(r'^dataset/$', views.datasetlist, name='datasetlist'),
	url(r'^api/data/$', views.get_data, name='api-data'),
	url(r'^charts/$', chart_views.chart, name='chart'),
	url(r'^chart/(?P<dataset_name>\D+)/$', chart_views.get_visualization,name='visualization'),
	url(r'^saveGraph/$', chart_views.saveVisualization,name='save-visualization'),
	url(r'^getVisualization/$', chart_views.getVisualizationList,name='get-visualization'),
	url(r'^api/chart/data/(?P<dataset_name>\D+)/$', chart_views.visualization_data,name='visualization-data'),
	url(r'^api/chart/data/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', chart_views.get_data,name='chart-data'),
	url(r'^chart/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', chart_views.makechart, name='aschart'),
	url(r'^upload/$', dataset_upload_views.upload, name='upload'),
	url(r'^giveDatasetName/$', dataset_upload_views.giveDatasetName, name='give-dataset-name'),
	url(r'^upload/fileType/$', dataset_upload_views.submitFiletype, name='submitFiletype'),
	url(r'^upload/dataType/$', dataset_upload_views.changeDataTypeInMongo, name='submitDatatype'),
	url(r'^getDataset/$', chart_views.getDataset, name='getDataset'),
	url(r'^getGraphFields/$', chart_views.getGraphFields, name='getGraphFields'),
	url(r'^getGraphData/$', chart_views.getGraphData, name='getGraphData'),
	url(r'^makeProcess/$', process_views.makeProcess, name='makeProcess'),
	url(r'^getProcess/$', process_views.getProcess, name='getProcess'),
	url(r'^getProcessList/$', process_views.getProcessList, name='getProcessList'),
	url(r'^delete/(?P<dataset_name>\w+)/$', dataset_upload_views.deleteDataset,name='deleteDataset'),
	url(r'^updateVisualization/$', chart_views.editVisualisation, name='editVisualisation'),
	url(r'^delVisualization/(?P<id>\d+)/$', chart_views.delVisualization,name='delete-visualization'),
	url(r'^admin/', admin.site.urls),
	url(r'^account_activation_sent/$', accounts_views.account_activation_sent, name='account_activation_sent'),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		accounts_views.activate, name='activate'),
	#url(r'^pdf/$', PDFTemplateView.as_view(template_name='pdftest.html',filename='mypdf.pdf'), name='pdf'),	
	#url(r'^pdfresponse/$',MyPDFView.as_view(), name='pdfresponse'),
	url(r'^mysqlconnect/$', dataset_upload_views.mysqlconnect, name='mySqlConnector'),
	url(r'^saveStatistics/$',statistical_views.saveStatistics,name='saveStatistics'),
	url(r'^calculateStatistics/$',statistical_views.calculateStatistics,name='calculateStatistics'),
	url(r'^getStatistical/$', statistical_views.getStatisticalList,name='getStatistical'),	
	url(r'^delStatistical/(?P<id>\d+)/$', statistical_views.delStatistical,name='delete-statistical'),
	
	url(r'^saveAnalytics/$',statistical_views.saveAnalytics,name='saveAnalytics'),
	url(r'^calculateAnalytics/$',statistical_views.calculateAnalytics,name='calculateAnalytics'),
	url(r'^getAnalytical/$', statistical_views.getAnalyticalList,name='getAnalytical'),	
	url(r'^delAnalytical/(?P<id>\d+)/$', statistical_views.delAnalytical,name='delete-analytical'),
	
	url(r'^mlearn/$', ml_views.mlearn, name="mlearn"),

]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)