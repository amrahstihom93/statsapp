from django.shortcuts import render

# Create your views here.
def processmap(request):
    print("Processmap DUDE!!!")
    return render(request, 'pmap.html')