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
from django.urls import re_path
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
from processmap import views as processmap_views
from qtools import views as qualitytools_views
from django.contrib.auth import views as auth_views
#from wkhtmltopdf.views import PDFTemplateView

urlpatterns = [
	re_path(r'^$', views.home, name='home'),
	re_path(r'^test/$', views.hometest, name='main'),
	re_path(r'^makeCol/$', dataset_upload_views.makeCol, name='makeCol'),
	re_path(r'^signup/$', accounts_views.signup, name='signup'),
	#	url(r'^signup_success/$', accounts_views.signup_success, name='signup-success'),
	re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
	re_path(r'^dataset/$', views.datasetlist, name='datasetlist'),
	re_path(r'^api/data/$', views.get_data, name='api-data'),
	re_path(r'^charts/$', chart_views.chart, name='chart'),
	re_path(r'^chart/(?P<dataset_name>\D+)/$', chart_views.get_visualization,name='visualization'),
	re_path(r'^saveGraph/$', chart_views.saveVisualization,name='save-visualization'),
	re_path(r'^getVisualization/$', chart_views.getVisualizationList,name='get-visualization'),
	re_path(r'^api/chart/data/(?P<dataset_name>\D+)/$', chart_views.visualization_data,name='visualization-data'),
	re_path(r'^api/chart/data/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', chart_views.get_data,name='chart-data'),
	re_path(r'^chart/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', chart_views.makechart, name='aschart'),
	re_path(r'^upload/$', dataset_upload_views.upload, name='upload'),
	re_path(r'^giveDatasetName/$', dataset_upload_views.giveDatasetName, name='give-dataset-name'),
	re_path(r'^upload/fileType/$', dataset_upload_views.submitFiletype, name='submitFiletype'),
	re_path(r'^upload/dataType/$', dataset_upload_views.changeDataTypeInMongo, name='submitDatatype'),
	re_path(r'^getDataset/$', chart_views.getDataset, name='getDataset'),
	re_path(r'^getGraphFields/$', chart_views.getGraphFields, name='getGraphFields'),
	re_path(r'^getGraphData/$', chart_views.getGraphData, name='getGraphData'),
    re_path(r'^getSubgroup/$', chart_views.getSubgroup, name='getSubgroup'),
	re_path(r'^makeProcess/$', process_views.makeProcess, name='makeProcess'),
	re_path(r'^getProcess/$', process_views.getProcess, name='getProcess'),
	re_path(r'^getProcessList/$', process_views.getProcessList, name='getProcessList'),
	re_path(r'^delete/(?P<dataset_name>\w+)/$', dataset_upload_views.deleteDataset,name='deleteDataset'),
	re_path(r'^updateVisualization/$', chart_views.editVisualisation, name='editVisualisation'),
	re_path(r'^delVisualization/(?P<id>\d+)/$', chart_views.delVisualization,name='delete-visualization'),
	re_path(r'^admin/', admin.site.urls),
	re_path(r'^account_activation_sent/$', accounts_views.account_activation_sent, name='account_activation_sent'),
	re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		accounts_views.activate, name='activate'),
	#url(r'^pdf/$', PDFTemplateView.as_view(template_name='pdftest.html',filename='mypdf.pdf'), name='pdf'),
	#url(r'^pdfresponse/$',MyPDFView.as_view(), name='pdfresponse'),
	re_path(r'^mysqlconnect/$', dataset_upload_views.mysqlconnect, name='mySqlConnector'),
	re_path(r'^saveStatistics/$',statistical_views.saveStatistics,name='saveStatistics'),
	re_path(r'^calculateStatistics/$',statistical_views.calculateStatistics,name='calculateStatistics'),
	re_path(r'^getStatistical/$', statistical_views.getStatisticalList,name='getStatistical'),
	re_path(r'^delStatistical/(?P<id>\d+)/$', statistical_views.delStatistical,name='delete-statistical'),

	re_path(r'^saveAnalytics/$',statistical_views.saveAnalytics,name='saveAnalytics'),
	re_path(r'^calculateAnalytics/$',statistical_views.calculateAnalytics,name='calculateAnalytics'),
	re_path(r'^getAnalytical/$', statistical_views.getAnalyticalList,name='getAnalytical'),
	re_path(r'^delAnalytical/(?P<id>\d+)/$', statistical_views.delAnalytical,name='delete-analytical'),

    re_path(r'^calculateHypothesis/$',statistical_views.calculateHypothesis,name='calculateHypothesis'),
    re_path(r'^saveHypothesis/$',statistical_views.saveHypothesis,name='saveHypothesis'),
    re_path(r'^hypoList/$',statistical_views.hypoList,name='hypoList'),


	re_path(r'^mlearn/$', ml_views.mlearn, name="mlearn"),
    re_path(r'^calcsregression/$', ml_views.calcsregression, name='calcsregression'),
    re_path(r'^multiregression/$', ml_views.multiregression, name='multiregression'),
    re_path(r'^saveMLmodel/$', ml_views.saveMLmodel, name='calcsregression'),

    re_path(r'^mdep/$', ml_views.mlearn, name="mdep"),
    re_path(r'^mlist/$', ml_views.mlist, name="mlist"),
    re_path(r'^mldat/$', ml_views.mldat, name="mldat"),

    re_path(r'^processmap/$', processmap_views.processmap, name="processmap"),
    re_path(r'^open/$', processmap_views.processmapopen, name="processmap"),
    re_path(r'^save/$', processmap_views.processmapsave, name="save"),
    re_path(r'^qualityTools/$', qualitytools_views.qtools, name="qualitytools"),
    re_path(r'^opptracker/$', qualitytools_views.opptracker, name="opptracker"),
    re_path(r'^saveFMEA/$', qualitytools_views.saveFMEA, name="qualitytools_fmea"),
    re_path(r'^fmeaList/$', qualitytools_views.fmeaList, name="qualitytools_fmeaList")




]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
