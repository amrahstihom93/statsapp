from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.views import View
#from wkhtmltopdf.views import PDFTemplateResponse

def hometest(req):
    return render(req, 'main.html', {'STATIC_URL': settings.STATIC_URL})
	

def datasetlist(req):
    return render(req, 'datasetlist.html', {'STATIC_URL': settings.STATIC_URL})

	
def home(request):
    return render(request, 'home.html', {'STATIC_URL': settings.STATIC_URL})
	
def get_data(req):
	labels = ["Red", "Blue", "Yellow", "Green", "Purple"]
	default_items = [23,10,6,17,5]
	data = {
		"labels": labels,
		"default_items" : default_items,
	}
	return JsonResponse(data)

def chart(req):
	return render(req, 'chart.html',{'STATIC_URL': settings.STATIC_URL})
	
#class MyPDFView(View):
 #   template='pdftest.html'
 #   context= {'title': 'Hello World!'}

 #   def get(self, request):
 #       response = PDFTemplateResponse(request=request,
  #                                     template=self.template,
  #                                     filename="hello.pdf",
  #                                     context= self.context,
  #                                     show_content_in_browser=True,
  #                                     cmd_options={'margin-top': 50},
   #                                    )
   #     return response