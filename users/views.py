from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# users/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

#drf
from rest_framework import generics
from . import models
from . import serializers

#signals
from allauth.account.signals import user_signed_up, password_set
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from users.models import custom_verification_code as cvc
from random import randint
from users.models import CustomUser as user
from users.models import user_data
from rest_framework import viewsets

#email
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from rest_framework.permissions import IsAuthenticated
from .forms import CustomUserCreationForm
from django.http import JsonResponse
import json


from datetime import date
#from django.core import serializers

class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

#drf
class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

class profile_data(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.user_data.objects.all()
    serializer_class = serializers.userdataser


class user_profile(APIView):
    authentication_classes = [authentication.TokenAuthentication]
#    permission_classes = [permissions.IsAdminUser]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        pid = request.GET.get("profile_id")
        if pid is not None:
            try:
                i = models.user_data.objects.get(id = pid,active=True)
            except:
                return JsonResponse({"message":"Invalid profile id"}, status=400)
            if i.account_id != user:
                return JsonResponse({"message":"Current user cannot access this profile"}, status=400)
            type = ''
            if i.account_type==0:
                type = 'primary'
            if i.account_type==1:
                type = 'subuser'
            return JsonResponse({'profile':type,'id':i.id,'name':i.name,'dob':i.dob,'email':i.email,'gender':i.gender,'pregnancy':i.pregnancy,'relation':i.relation})

        profiles = models.user_data.objects.filter(account_id = user,active=True)
        plist = []
        for i in profiles:
            if i.account_type == 0:
                plist.append({'profile':'primary','id':i.id,'name':i.name,'dob':i.dob,'email':i.email,'gender':i.gender,'pregnancy':i.pregnancy,'relation':i.relation,'acount_id':user.id})
            else:
                plist.append({'profile':'subuser','id':i.id,'name':i.name,'dob':i.dob,'email':i.email,'gender':i.gender,'pregnancy':i.pregnancy,'relation':i.relation})
        return  JsonResponse(plist, safe=False)

    def post(self, request, format=None):
        user = request.user
        jdata =json.loads(request.body)
        if models.user_data.objects.filter(account_id=user).count() >= models.account_data.objects.get(user=user).subusers_allowed:
            return JsonResponse({"message":"Your limit of subusers has reached based on your plan"}, status=400)
        if not all(elm in list(jdata.keys()) for elm in ['name','dob','gender','pregnancy','primary']):
            return JsonResponse({"message":"Not all required variables are provided"}, status=400)
        if jdata['primary']==True: #not models.user_data.objects.filter(account_id=user.id).count():
            if models.user_data.objects.filter(account_id=user,account_type=0).count():
               return JsonResponse({"message":"user already has a primary profile"}, status=400)    
            record = models.user_data.objects.create(account_type=0,name = jdata['name'],dob = jdata['dob'],gender = jdata['gender'],pregnancy = jdata['pregnancy'],account_id=user)
            record.email=user.email
            if 'relation' in jdata.keys():
                record.relation=jdata['relation']
            record.save()
            message = 'primary profile successfully created'
        else:
            record = models.user_data.objects.create(account_type=1,name = jdata['name'],dob = jdata['dob'],gender = jdata['gender'],pregnancy = jdata['pregnancy'],account_id=user)
            if 'email' in jdata.keys():
                record.email=jdata['email']
                record.save()
            if 'relation' in jdata.keys():
                record.relation=jdata['relation']
                record.save()
            message = 'subuser profile is successfully created'
        return  JsonResponse({'message':message,'profile_id':record.id}, safe=False)

    def patch(self, request, format=None):
        user = request.user
        jdata =json.loads(request.body)
        pid = request.GET.get("profile_id")
        if pid is None:
            return JsonResponse({"message":"Profile id not provided"}, status=400)
        try:
            i = models.user_data.objects.get(id = pid)
        except:
            return JsonResponse({"message":"Invalid profile id"}, status=400)
        if i.account_id != user:
            return JsonResponse({"message":"Current user cannot access this profile"}, status=400)
        if not all(elm in list(jdata.keys()) for elm in ['name','dob','gender','pregnancy']):
            return JsonResponse({"message":"Not all required variables are provided"}, status=400)
        i.name = jdata['name']
        i.dob = jdata['dob']
        i.gender = jdata['gender']
        i.pregnancy = jdata['pregnancy']
        if 'email' in jdata.keys():
            i.email = jdata['email']
        if 'relation' in jdata.keys():
            i.relation = jdata['relation']
        i.save() 
        return  JsonResponse({"message":"Details updated successfully"})


    def delete(self, request, format=None):
        user = request.user
        pid = request.GET.get("profile_id")
        if pid is None:
            return JsonResponse({"message":"Profile id not provided"}, status=400)
        try:
            i = models.user_data.objects.get(id = pid)
        except:
            return JsonResponse({"message":"Invalid profile id"}, status=400)
        if i.account_id != user:
            return JsonResponse({"message":"Current user cannot access this profile"}, status=400)
        if i.account_type == 0:
            return JsonResponse({"message":"Primary profile cannot be deleted"}, status=400)
        i.active = False
        i.save()
        return JsonResponse({"message":"Successfully deleted the user profile"}) 

#email checkup
def emailcheck(request):
    try:
        email = request.GET['email']
    except:
        return JsonResponse({"message":"Required Details are not provided"}, status=400)
    if user.objects.filter(email=email).count():
        i = user.objects.get(email=email)
        return JsonResponse({"message":"Email is already registered","account_id":i.id}, status=403)
    else:
        return JsonResponse({"message":"Email is Not Registered"})
#    serializer_class = serializers.UserSerializer


#send mail
@receiver(user_signed_up)
def send_code(sender, **kwargs):
    # username = kwargs['request'].user.username
    email = kwargs['user'].email
    username = kwargs['user'].username
#    firstname = kwargs['user'].firtst
#    kkk = user.objects.get(email=email)
#    models.account_data.objects.create(user=kkk)
    code = randint(100000, 999999)
    while cvc.objects.filter(code=code).exists():
        code = code + 1
    record = cvc(email=email,code=code)
    rr = user.objects.get(email=email)
    models.account_data.objects.create(user=rr)
    
    rr.is_active = False
    record.save()
    rr.save()
    content = 'Thanks for signing up for Dr. sila Please enter the following code to complete the signup process'
    html_message = render_to_string('email_template_en.html', {'code': code,'content':content,'username':username})
    plain_message = strip_tags(html_message)
    send_mail('Dr.Sila Verification code - {}'.format(code),plain_message,'accounts@drsila.com',[email],html_message=html_message,fail_silently=False)
    return
#class verify


def useractivate(request):
    try:
        code = request.GET['code']
        email = request.GET['email']
    except:
        return JsonResponse({"message":"Required Details are not provided"}, status=403)
    try:
        scode =  cvc.objects.get(email=email)
    except:
        if user.objects.filter(email=email).count():
            if user.objects.get(email=email).is_active:
                return JsonResponse({"message":"Email aready activated"}, status=403)
            else:
                return JsonResponse({"message":"Unable find the user"}, status=403)
        else:
            return JsonResponse({"message":"Email not registered "}, status=403)

    if str(code) == str(scode.code):
        scode.delete()
        rr = user.objects.get(email=email)
        rr.is_active = True
        rr.save()
        return JsonResponse({"message":"user activated","account_id":rr.id})
    else:
        return JsonResponse({"message":"Code incorrect"}, status=403)

def resend_activation(request):
    try:
        email = request.GET['email']
    except:
        return JsonResponse({"message":"Required Details are not provided"}, status=403)
    if not user.objects.filter(email=email).count():
        return  JsonResponse({"message":"email is not yet registered"}, status=403)
    rr = user.objects.get(email=email)
    if rr.is_active:
        return  JsonResponse({"message":"User is already activated"}, status=403)
    if not  cvc.objects.filter(email=email).count():
        return  JsonResponse({"message":"code not found in the database, please contact support"}, status=403) 

    scode = cvc.objects.get(email=email)
    username = rr.username
    code = scode.code
    try:
        content = 'Thanks for signing up for Dr. sila Please enter the following code to complete the signup process'
        html_message = render_to_string('email_template_en.html', {'code': code,'content':content,'username':username})
        plain_message = strip_tags(html_message)
        send_mail('Dr.Sila Verification code - {}'.format(code),plain_message,'accounts@drsila.com',[email],html_message=html_message,fail_silently=False)
        return JsonResponse({"message":"Verification code resent successfully"})
    except:
        return JsonResponse({"message":"Something Went wrong"}, status=403)



class coupon_redeem(APIView):
    authentication_classes = [authentication.TokenAuthentication]
#    permission_classes = [permissions.IsAdminUser]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        edit_profile = EditProfileForm(user=user)
        redeem = CouponForm()
        if request.method == 'POST':
            edit_profile = EditProfileForm(request.POST, user=user)
            redeem = CouponForm(request.POST, user=user)
            if redeem.is_valid():
                coupon = redeem.coupon
                coupon.redeem(request.user)
            else:
                pass
            return render(request, 'main/profile.html', {'edit_profile': edit_profile, 'redeem': redeem})

        return render(request, 'main/profile.html', {'edit_profile': edit_profile, 'redeem': redeem})
    
class plan_update(APIView):
#    authentication_classes = [authentication.TokenAuthentication]
#    permission_classes = [permissions.IsAdminUser]
#    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = json.load(request.body)
        if not all(elm in list(data.keys()) for elm in ['plan_id','user_id']):
            return JsonResponse({"message":"required details are not provided not provided"}, status=400)
        try:
            i = models.subscription_plans.objects.get(id = data['plan_is'])
        except:
            return JsonResponse({"message":"Invalid plan id"}, status=400)
        user = user.objects.get(id=data['user_id'])
        adata = models.account_data.objects.get(user=user)
        adata.reports_allowed =i.allowed_reports
        adata.report_check =i.infinate_reports
        adata.subusers_allowed=i.allowed_subusers
        adata.subuser_check=i.infinate_subusers
        enddate = date + timedelta(days=i.extension_days)
        startdate = date.today
        adata.save()
        return JsonResponse({"message":"Plan updated successfully"})
    def get(self, request):
        data = models.subscription_plans.objects.filter(active=True)
        plans = []
        for i in data:
            plan = {}
            plan['days'] = None
            plan['reports_allowed'] = None
            plan['profiles_allowed'] = None
            plan['id'] = i.id
            if not i.infinate_reports:
                plan['reports_allowed']= i.allowed_reports
            if not i.infinate_days:
                plan['days'] = i.extension_days
            if not i.infinate_subusers:
                plan['profiles_allowed'] = i.allowed_subusers
            plan['description']=i.description
            plans.append(plan)
        return JsonResponse({"plans":plans})
 

