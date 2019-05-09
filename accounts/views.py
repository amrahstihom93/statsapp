from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import SignUpForm
from accounts.models import ClientList
from process.models import Process, Process_List
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
import datetime


def signup(request):
    # datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    client = ClientList()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(request.POST)
        print('before validation')
        if form.is_valid():
            print(request.POST)
            adminflag = False
            if request.POST['firm'] == 'company':
                if request.POST['company'] == 'new company':
                    client.company_name = request.POST['company_name']
                    client.email_id = request.POST['email']
                    client.client_id = 'CID' + client.company_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    print("hey it here clint", client.client_id)
                    client.save()
                    adminflag = True
                elif request.POST['company'] == 'old company':
                    comp_code = request.POST.get('company_name')
                    temp_client = ClientList.objects.filter(client_id__exact="%s" % comp_code)
                    if temp_client.count() == 1:
                        client = temp_client
                    else:
                        form = SignUpForm()
                        return render(request, 'signup.html', {'form': form})
                    print("from vie wprinting client", client.values())
                    print("from vie wprinting client 000", client[0])
                    print("from vie wprinting client 00011", client)

            elif request.POST['firm'] == 'individual':
                client.company_name = 'INDI' + request.POST['username']
                client.email_id = request.POST['email']
                client.client_id = client.company_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                client.save()
                adminflag = True
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # print('hey from body ', request.body)
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            # print('helllooooooooooooossss 33')
            user.profile.is_admin = adminflag
            # print('helllooooooooooooossss 44')
            # print(client.client_id)
            user.profile.client = client
            user.is_active = False
            # print('helllooooooooooooossss 99   ', user.profile.client.client_id)
            user.save()
            subject = 'Activate Your MySite Account'

            current_site = get_current_site(request)
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # user.email_user(subject, message)
            emailid = []
            emailid.append(client.email_id)
            print(type(emailid))
            print(emailid)
            print(type(client.email_id))
            send_mail(subject, message, 'mohitsigmaway123@gmail.com', emailid)
            msg = 'Account is created successfully and activation link is sent on your email-id'
            result=createRootProcess(user, client)
            print(result)
            return render(request, 'signup-success.html', {'success_msg': msg})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        msg = 'Account verified'
        return render(request, 'signup-success.html', {'success_msg': msg})
    else:
        return render(request, 'account_activation_invalid.html')


def signup_success(request):
    return render(request, 'signup-success.html')


def createRootProcess(user, client):
    try:
        processlist = Process_List()
        process = Process()
        process.process_id = 'PIDroot'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        process.process_name = 'root'
        process.parent_p_id = 'PID00000000000000'
        process.client_id = client
        process.user_id = user
        process.save()
        processlist.process_id = process
        processlist.user_id = user
        processlist.save()
        return 'Root process created successfully!!'
    except:
        return 'Root process not created!!'
