from django.shortcuts import render, redirect
from .forms import SignUpForm
from accounts.models import ClientList
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
import datetime
def signup(request):
    # datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request.POST)
        print('before validation')
        if form.is_valid():
            print(request.POST)
            client = ClientList()
            adminflag =False
            if request.POST['firm'] == 'company':
                if request.POST['company'] == 'new company':
                    client.company_name = request.POST['company_name']
                    client.email_id = request.POST['email']
                    client.client_id = 'CID'+client.company_name+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    print("hey it here clint", client.client_id)
                    client.save()
                    adminflag = True
                elif request.POST['company'] == 'old company':
                    comp_code = request.POST.get('company_name')
                    temp_client = ClientList.objects.filter(client_id__exact="%s"%comp_code)
                    if temp_client.count() == 1:
                        client = temp_client
                    else:
                        form = SignUpForm()
                        return render(request, 'signup.html', {'form': form})
                    print("from vie wprinting client", client.values())
                    print("from vie wprinting client 000", client[0])
                    print("from vie wprinting client 00011", client)

            elif request.POST['individual'] == 'on':
                client.company_name = 'INDI'+ request.POST['username']
                client.email_id = request.POST['email']
                client.client_id = client.company_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                client.save()
                adminflag = True
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # print('hey from body ', request.body)
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            # print('helllooooooooooooossss 33')
            user.profile.is_admin =adminflag
            # print('helllooooooooooooossss 44')
            # print(client.client_id)
            user.profile.client = client
            # print('helllooooooooooooossss 99   ', user.profile.client.client_id)
            user.save()
            msg = 'Account is created successfully'
            return render(request, 'signup-success.html', {'success_msg': msg})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signup_success(request):
    return render(request, 'signup-success.html')