from django.shortcuts import render

# Create your views here.
def processmap(request):
    print("Processmap DUDE!!!")
    return render(request, 'pmap.html')
def processmapopen(request):
    print("open")
    return render(request, 'open.html')
def processmapsave(request):
    print("save")
    return render(request, 'save.html')
