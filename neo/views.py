from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from django.http import JsonResponse
import pickle



from . import models
from . import serializers
from neomodel import db
from api.models import settings as apisettings
from user.models import account_data,reports 
from collections import Counter
import pandas as pd
import json


from users.models import CustomUser as user


QA_SYMPTOM_SEND = 10
QA_DISEASE_SEND = 5
QA_STOP_DISEASE_COUNT = 3
QA_STOP_LOOP_COUNT = 15

class Symptom(generics.ListCreateAPIView):
    queryset = models.Symptom.nodes.all()
    serializer_class = serializers.Symptom


class getsyms(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated)
    def get(self, request, format=None):
        return HttpResponse(models.Symptom.nodes.all())



class userview(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated)

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)



class qa(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def makequery_ar(self,sl):
        q = '''MATCH (u:User {group: $age, gender: $gen, pregnancy: $preg}) WITH u'''
        for i in range(len(sl)):
            q = q + ''' MATCH (:Symptom {ar_name: "'''+ sl[i] +'''"})<-[:has]-(d:Disease) WITH d'''
        q = q + ''' Match (d:Disease)-[:has]->(ps:Symptom) return d.ar_name , ps.ar_name'''
        return q
    def makequery(self,sl):
        q = '''MATCH (u:User {group: $age, gender: $gen, pregnancy: $preg}) WITH u'''
        for i in range(len(sl)):
            q = q + ''' MATCH (:Symptom {name: "'''+ sl[i] +'''"})<-[:has]-(d:Disease) WITH d'''
        q = q + ''' Match (d:Disease)-[:has]->(ps:Symptom) return d.name , ps.name''' #,ps.description
        return q
    def getdescription(self,li,ar=False):
        if ar:
            result, meta = db.cypher_query('match (s:Symptom) where s.ar_name in $symlist return s.ar_name,s.ar_description',{'symlist':li})
        else:
            result, meta = db.cypher_query('match (s:Symptom) where s.name in $symlist return s.name,s.description',{'symlist':li})
        return result
    def getprobs(self,li,skip):
        _ = pd.DataFrame(li,columns=['Disease','Symptom'])
        r = _.groupby('Disease').size().div(len(_)).sort_values(ascending=False)
        disprob = {}
        for i in range(len(list(r[:QA_DISEASE_SEND].index))):
            disprob[r.index[i]] = r[i]
#        Counter(_['Symptom']).most_common(skip+QA_SYMPTOM_SEND)[skip:QA_SYMPTOM_SEND]
        symcounter = Counter(_['Symptom']).most_common(skip+QA_SYMPTOM_SEND)[skip:QA_SYMPTOM_SEND]
        symlist = []
        for i in symcounter:
            symlist.append(i[0])
        return  symcounter,disprob,symlist #Counter(_['Symptom']).most_common(10),disprob

    def post(self, request, format=None):
        data = request.data
        ar = False
        if not all(elm in list(data.keys()) for elm in ['age','gender','pregnancy','symtomps']):
            return JsonResponse({"message":"required parameters are not provided"}, status=400)
        params = {'age':data['age'],'gen':data['gender'],'preg':data['pregnancy']}
        if 'language' in data.keys():
            if data['language']!='ar':
                return JsonResponse({"message":"Undefined Language"}, status=400)
            results, meta = db.cypher_query(self.makequery_ar(data['symtomps']),params)
            ar=True
        else:
            results, meta = db.cypher_query(self.makequery(data['symtomps']),params)
        if 'skip' in  data.keys():
            nextsyms,disprobs,symlist = self.getprobs(results,skip=data['skip'])
        else:
            nextsyms,disprobs,symlist = self.getprobs(results,skip=0)
        res = {'Disease_probabilities':disprobs,'Next_questions':nextsyms,'Descriptions':self.getdescription(symlist,ar)}
        return JsonResponse(res)

#         return HttpResponse(list(data.keys()))
#         return HttpResponse(models.Symptom.nodes.all())
#         age = request.POST.get('age')
#         gen = request.POST.get('gender')
#         preg = request.POST.get('pregnancy')
#         syms = request.POST.getlist('symtomps[]')


class symsearch1(APIView):

    def post(self, request, format=None):
        data = request.data
        if 'symptom' not in data.keys():
            return JsonResponse({"message":"required parameters are not provided"}, status=400)
        res = []
        if 'language' in data.keys():
            if data['language']!='ar':
                return JsonResponse({"message":"Undefined Language"}, status=400)
            with open('arlist.pkl', 'rb') as f:
                symlist = pickle.load(f)
        else:
            with open('enlist.pkl', 'rb') as f:
                symlist = pickle.load(f)
        li = list(filter(lambda x: data['symptom'] in x, symlist))
        for i in li:
            res.append([i,symlist[i]])
        return JsonResponse({"symptoms":res,"stop_disease_count":QA_STOP_DISEASE_COUNT,"stop_loop_count":QA_STOP_LOOP_COUNT})


class getsymptom(APIView):
    def post(self, request, format=None):
        data = request.data
        if 'symptom' not in data.keys():
            return JsonResponse({"message":"required parameters are not provided"}, status=400)
        params = {'sym':data['symptom']}
        if 'language' in data.keys():
            if data['language']!='ar':
                return JsonResponse({"message":"Undefined Language"}, status=400)
            results, meta = db.cypher_query("match (s:Symptom) where s.ar_name=$sym return s.ar_name,s.ar_description",params)
        else:
            results, meta = db.cypher_query("match (s:Symptom) where s.name=$sym return s.name,s.description",params)
        return JsonResponse({"symptoms":results})


#class symsearch(APIView):
#    def post(self, request, format=None):
#        data = request.data
#        if 'symptom' not in data.keys():
#            return JsonResponse({"message":"required parameters are not provided"}, status=400)
#        params = {'sym':data['symptom']}
#        if 'language' in data.keys():
#            if data['language']!='ar':
#                return JsonResponse({"message":"Undefined Language"}, status=400)
#            results, meta = db.cypher_query("match (s:Symptom) where s.ar_name contains $sym return s.ar_name,s.ar_description",params)
#        else:
#            results, meta = db.cypher_query("match (s:Symptom) where s.name contains $sym return s.name,s.description",params)
##         nextsyms,disprobs = self.getprobs(results)
#        res = {'symptoms':results}
#        return JsonResponse(res)


def makesymsearch(request):
    results, meta = db.cypher_query("match (s:Symptom) return s.name,s.ar_name,s.synonyms,s.ar_synonyms")
    _ = pd.DataFrame(results,columns=['name','ar_name','synonyms','ar_synonyms'])
    arlist ={}
    enlist = {}
    for index, row in _.iterrows():
        if row['synonyms']:
            for i in row['synonyms']:
                enlist[i] = row['name']
            enlist[row['name']] = row['name']
        else:
            enlist[row['name']] = row['name']
        if row['ar_synonyms']:
            for i in row['ar_synonyms']:
                arlist[i] = row['ar_name']
                arlist[row['ar_name']] = row['ar_name']
        else:
            arlist[row['ar_name']] = row['ar_name']
    with open('enlist.pkl', 'wb') as f:
        pickle.dump(enlist, f, pickle.HIGHEST_PROTOCOL)
    with open('arlist.pkl', 'wb') as f:
        pickle.dump(arlist, f, pickle.HIGHEST_PROTOCOL)
    return HttpResponse('Successfully updated symptom serach')


class getreport(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def getdiseasesdata(diseases,ar):
        if ar:
            result, meta = db.cypher_query('match (s:Disease) where s.ar_name in $dislist return s.ar_name,s.ar_description',{'symlist':li})
        else:
            result, meta = db.cypher_query('match (s:Disease) where s.name in $dislist return s.name,s.description',{'symlist':li})
        return result
    def post(self, request):
        user = request.user
        data = json.load(request.body)
        if not all(elm in list(data.keys()) for elm in ['symptomps','pofile_id','diseases']):
            return JsonResponse({"message":"required details are not provided not provided"}, status=400)
        ad = account_data.objects.get(user=user)
        try:
            pd = user_data.objects.get(id = data['pofile_id'])
        except:
            return JsonResponse({"message":"Invalid profile id"}, status=400)
        if pd.account_id != user:
            return JsonResponse({"message":"Current user cannot access this profile"}, status=400)
        if date.today() > ad.enddate:
            return JsonResponse({"message":"Your plan expired, please renew the plan"}, status=400)
        if ad.report_check:
            if not ad.reports_allowed:
                ad.reports_allowed = ad.reports_allowed-1
            else:
                return JsonResponse({"message":"Your cannot make more reports, please renew the plan"}, status=400)
        ad.report_count = ad.report_count + 1
        pd.report_count = pd.report_count + 1
        symptomps = ','.join(data['symptomps']
        diseases = ','.join(data['diseases']
        report = reports(user=user,profile=pd,symptomps=symptomps,diseases=diseases)
        ar = False
        if 'language' in data.keys():
            if data['language']!='ar':
                return JsonResponse({"message":"Undefined Language"}, status=400)
            ar = True
        
        return
