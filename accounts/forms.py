from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import RadioSelect
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from accounts.models import ClientList, Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, widget=forms.EmailInput())
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget, help_text='Max 10 digits')
    firm_choices = [('company', 'company'), ('individual', 'individual')]
    company_choices = [('new company', 'new company'), ('old company', 'old company')]
    firm = forms.ChoiceField( choices=firm_choices, widget=forms.RadioSelect(attrs={'id': 'id_firm', 'onclick': 'FirmType()'}))
    company = forms.ChoiceField(choices=company_choices, widget=forms.RadioSelect(attrs={'id': 'id_company', 'onclick': 'CompanyCheck()'}))
    company_name = forms.CharField(max_length=50, required= False, widget=forms.TextInput())
    # company_code = forms.CharField(max_length=50, widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'firm', 'company', 'company_name', 'phone_number', 'password1', 'password2')

    def clean_phone_number(self):
        print('in phone verification')
        phone_number = self.cleaned_data.get('phone_number')
        print(phone_number)
        profile = Profile()
        count = Profile.objects.filter(phone_number__exact="%s"%phone_number).count()
        print(count)
        if count > 0:
            raise ValidationError("phone number already linked to another account")
        return phone_number


    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        firm = self.cleaned_data.get('firm')
        company = self.cleaned_data.get('company')
        print(company)
        print(company_name)
        client = ClientList()
        # print('from clean method' + company_name)
        # print('from clean method' + company)
        # if 0 == 0:
        #     raise ValidationError("test error")
        if firm == 'company':
            if company == 'new company':
                print('from clean method 0')
                count = ClientList.objects.filter(company_name__exact="%s"%company_name).count()
                if count == 1:
                    print('from clean method 00')
                    raise ValidationError("Company already exist")
                elif count > 1:
                    print('from clean method 01')
                    raise ValidationError("Multiple company found!! Please report admin")
            elif company == 'old company':
                print('from clean method 1')
                if ClientList.objects.filter(client_id__exact="%s"%company_name).count() == 0:
                    print('from clean method 2')
                    raise ValidationError("No company exist")
        return company_name

    def clean_email(self):
        print('from clean email method')
        email= self.cleaned_data.get('email')
        company = self.cleaned_data.get('company')
        user_email_count = User.objects.filter(email__exact="%s" % email).count()
        client_email_count = ClientList.objects.filter(email_id__exact="%s" % email).count()
        if user_email_count > 0:
            raise ValidationError("User Email ID already exist")
        elif client_email_count > 0:
            raise ValidationError("Client Email ID already exist")
        return email
