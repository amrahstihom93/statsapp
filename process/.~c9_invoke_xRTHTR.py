from django.http import HttpResponse, JsonResponse
#from django.shortcuts import render
from .models import Process, Process_List
from upload.models import Dataset
from django.views.decorators.csrf import csrf_exempt
import json, datetime
from accounts.models import ClientList, Profile
from django.contrib.auth.models import User

def getProcess(request):
	print("in get Process")
	msg=''
	try:
		listObj = []
		usr = request.user
#		list = Process.objects.filter(user_id=usr).values()
		list = Process.objects.get(user_id=request.user.id).values()
		pr
		if len(list) > 0:
			for i in range(len(list)):
				listObj.append(list[i])
			print(listObj)
	#	print('successfully')
		return JsonResponse(listObj,safe=False)
	except:
		msg = 'error while getting process list'
		print(msg)
	return HttpResponse(msg)
	
@csrf_exempt
def makeProcess(request):
	print("in processs")
	msg = ''
	try:
		if request.method == 'POST':
			form = Process()
			form1 = Process_List()
			print("in process")
			form.process_name = request.POST['process_name']
			print(request.POST['process_name'])
			print(datetime.datetime.now())
			process_id = 'PID'+form.process_name+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
			print(process_id)
			form.process_id = process_id
			id = request.user.id
			print(' hey we here before', id)
			user_obj = User.objects.get(pk=id)
			# print(' hey we here')
			# print(user_obj.email)
			# username=request.user
			# print('user info from process',username)
			# print('user info from process',username.username)
			# print('user info from process',username.email)
			# print('user info from process',username.profile.phone_number)
			# print('user info from process',username.id)
			# #form.user_id = str(request.user)
			form.user_id = user_obj
			client=user_obj.profile.client
			print('client id', client.client_id)
			form.client_id = client
			form.parent_p_id = request.POST['parent_process']
			print(form.parent_p_id)
			temp_process = Process.objects.get(process_id=process_id).values
			temp_process = Process.objects.get(process_id=process_id)
			print('temp pro')
			print(temp_process)
			print('hello ',temp_process.process_name)
			form1.process_id = temp_process	
			print('hello 1', temp_process)
			#form1.user_id = form.user_id
			form1.user_id = user_obj
			print('hello 2')
			# form.save()
			form1.save()
			print('hello 3')
			msg = 'process saved successfully'
			print(msg)
	except:
		msg = 'error occurred while saving'
		print(msg)
	return HttpResponse(msg)

def getProcessList(request):
	print("in get ProcessList")
	msg=''
	try:
		listObj = []
		datasetObj = []
		responseObj = []
		usr = request.user
		list = Process.objects.filter(user_id=usr.id,parent_p_id=request.POST['parent_process']).values()
		if len(list) > 0:
			for i in range(len(list)):
				listObj.append(list[i])
			print(listObj)
	#	print('successfully')
		responseObj.append(listObj)
		list = Dataset.objects.filter(user_id=usr, process_id=request.POST['parent_process']).values()
		if len(list) > 0:
			for i in range(len(list)):
				datasetObj.append(list[i])
			print(datasetObj)
		responseObj.append(datasetObj)
		return JsonResponse(responseObj,safe=False)
	except:
		msg = 'error while getting process list'
		print(msg)
	return HttpResponse(msg)