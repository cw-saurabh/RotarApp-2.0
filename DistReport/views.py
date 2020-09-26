from django.shortcuts import render
from Auth.models import DistrictCouncil, Member, DistrictRole
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DistReport, Task, Response, Month
import json
from django.db import transaction
import datetime

year = datetime.datetime.now().year
reportingMonth = '09'

def admin_getMonth(request):
    months = Month.objects.filter(view=True).order_by('year','month').all()
    council = dict()
    roleList = DistrictRole.objects.all()
    for role in roleList :
        count = DistrictCouncil.objects.filter(districtRole=role).count()
        if count==1:
            person = DistrictCouncil.objects.filter(districtRole=role).first()
            memberProfiles = Member.objects.filter(login=person.accountId).first()
        else :
            people = DistrictCouncil.objects.filter(districtRole=role).all()
            memberProfiles = []
            for person in people :
                memberProfile = Member.objects.filter(login=person.accountId).first()
                memberProfiles.append(memberProfile)
        
        council1 = {}
        council1['count'] = count
        council1['data'] = memberProfiles
        council[role] = council1

    return render(request, 'DistReport/getMonth.html',{'title':'Tasks','Tab':'Tasks','DRole':'0','Council':council,'Months':months})

def admin_getTasks(request, monthId, distRoleId):
    districtRole = DistrictRole.objects.filter(distRoleId=distRoleId).first()
    month = Month.objects.filter(id=monthId).first()
    reportId = month.month+"-"+month.year+"-"+str(districtRole.distRoleId)
    report, created = DistReport.objects.get_or_create(dReportId=reportId, month=month, districtRole=districtRole)
    response = Response.objects.filter(dReport=report).all().values_list('responseId','task__taskId','task__taskText','driveLink','completionStatus','response','modifiedOn','allottedBy')
    return render(request, 'DistReport/getTasks.html',{'title':'Tasks','Tab':'Tasks','DRole':'0','Response':response,'DistrictRole':districtRole,'ReportId':report.dReportId,'Month':month})

def admin_addTask(request):
    
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
            newTask = Task(taskText=data['taskText'])
            newTask.save()
        
            # districtRole = DistrictRole.objects.filter(distRoleId=data['DistrictRoleId']).first()
            report = DistReport.objects.filter(dReportId=data['ReportId']).first()
        
            newResponse = Response(dReport = report, task = newTask)
            newResponse.save()

        jsonResponse = {}
        response = Response.objects.filter(dReport=report).values('responseId','task__taskId','task__taskText','completionStatus','response','driveLink','modifiedOn','allottedBy')
        for item in response :
            jsonResponse[item['responseId']] = item

        data = {
            'success': True,
            'tasks':jsonResponse
        }

    except Exception as Error :
        print(Error)
        data = {
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }
        
    return JsonResponse(data)

def admin_deleteTask(request):
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
            # districtRole = DistrictRole.objects.filter(distRoleId=data['DistrictRole']).first()
            report = DistReport.objects.filter(dReportId=data['ReportId']).first()
            Response.objects.filter(responseId=data['ResponseId']).delete()

        jsonResponse = {}
        response = Response.objects.filter(dReport=report).values('responseId','task__taskId','task__taskText','completionStatus','response','driveLink','modifiedOn','allottedBy')
        for item in response :
            jsonResponse[item['responseId']] = item

        data = {
            'success': True,
            'tasks':jsonResponse
        }

    except Exception as Error :
        data = {
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }
        
    return JsonResponse(data)

def admin_editTask(request):
    
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
            # districtRole = DistrictRole.objects.filter(distRoleId=data['DistrictRole']).first()
            report = DistReport.objects.filter(dReportId=data['ReportId']).first()
            Task.objects.filter(taskId=data['taskId']).update(taskText=data['taskText'])

        jsonResponse = {}
        response = Response.objects.filter(dReport=report).values('responseId','task__taskId','task__taskText','completionStatus','response','driveLink','modifiedOn','allottedBy')
        for item in response :
            jsonResponse[item['responseId']] = item

        data = {
            'success': True,
            'tasks':jsonResponse
        }

    except Exception as Error :
        data = {
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }
        
    return JsonResponse(data)

def council_index(request):
    months = Month.objects.filter(view=True).order_by('year','month').all()
    Council = DistrictCouncil.objects.filter(accountId = request.user).first()
    return render(request, 'DistReport/index.html',{'title':'Tasks','Tab':'Tasks','DRole':'1','DistRole':Council.districtRole.distRoleName,'Months':months})

def council_getTasks(request):
    months = Month.objects.filter(view=True).order_by('year','month').all()
    print("hii")
    print(months)    
    Council = DistrictCouncil.objects.filter(accountId = request.user).first()
    
    report = DistReport.objects.filter(districtRole = Council.districtRole)
    
    try :
        jsonResponse = {}
        
        for month in months :
            
            jsonResponse[month.id] = {}

            report1 = report.filter(month=month).first()
            
            response1 = Response.objects.filter(dReport=report1).values('responseId','task__taskId','task__taskText','completionStatus','response','driveLink','modifiedOn','allottedBy')
            
            for item in response1 :
                jsonResponse[month.id][item['responseId']] = item

        data = {
            'success': True,
            'tasks':jsonResponse
        }

        print(jsonResponse)

    except Exception as Error :
        print(Error)
        data = {
            'success': False,
            'error' : "An error has occurred, Contact the website coordinators"
        }
        
    return JsonResponse(data)

def council_saveTask(request):

    data = json.loads(request.POST.get('data'))
    
    task = data['data']

    try :
        
        response = Response.objects.filter(responseId = data['responseId'])
        print(response)
        response.update(modifiedOn=datetime.datetime.now(), **task)
    
    except Exception as e :
        print(e)
        data = {
            'success': False,
            'error' : "An error has occurred, Contact the website coordinators"
        }
        return JsonResponse(data)

    Council = DistrictCouncil.objects.filter(accountId = request.user).first()

    report = DistReport.objects.filter(districtRole = Council.districtRole)
    
    try :
        jsonResponse = {}
        months = Month.objects.filter(view=True).order_by('year','month').all()
        for month in months :
            
            jsonResponse[month.id] = {}

            report1 = report.filter(month=month).first()
            
            response1 = Response.objects.filter(dReport=report1).values('responseId','task__taskId','task__taskText','completionStatus','response','driveLink','modifiedOn','allottedBy')
            
            for item in response1 :
                jsonResponse[month.id][item['responseId']] = item

        data = {
            'success': True,
            'tasks':jsonResponse
        }

    except Exception as Error :
        print(Error)
        data = {
            'success': False,
            'error' : "An error has occurred, Contact the website coordinators"
        }
        
    return JsonResponse(data)

def council_addTask(request):

    try :
        
        data = json.loads(request.POST.get('data'))
        
        Council = DistrictCouncil.objects.filter(accountId = request.user).first()
        print(data['monthId'])

        month = Month.objects.filter(id=data['monthId']).first()
        reportId = month.month+"-"+month.year+"-"+str(Council.districtRole.distRoleId)
        print(reportId)

        with transaction.atomic() :
            
            newTask = Task(taskText=data['taskText'])
            newTask.save()

            Council = DistrictCouncil.objects.filter(accountId = request.user).first()
            report = DistReport.objects.filter(dReportId = reportId)
            
            if report.exists() :
                newResponse = Response(dReport = report.first(), task = newTask, allottedBy = '1')
                newResponse.save()

            else :
                report = DistReport(districtRole=Council.districtRole, month=month, dReportId=reportId) 
                report.save()
                newResponse = Response(dReport = report, task = newTask, allottedBy = '1')
                newResponse.save()

        jsonResponse = {}
        months = Month.objects.filter(view=True).order_by('year','month').all()
        for month in months :
            
            jsonResponse[month.id] = {}

            report1 = report.filter(month=month).first()
            
            response1 = Response.objects.filter(dReport=report1).values('responseId','task__taskId','task__taskText','completionStatus','response','driveLink','modifiedOn','allottedBy')
            
            for item in response1 :
                jsonResponse[month.id][item['responseId']] = item

        data = {
            'success': True,
            'tasks':jsonResponse
        }


    except Exception as Error :
    
        print(Error)
        data = {
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }
        
    return JsonResponse(data)

