from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
def qtools(request):
    print("Quality Tools DUDE!!!")
    return render(request, 'qtools.html')
def opptracker(request):
    return render(request, 'opptrack.html')
