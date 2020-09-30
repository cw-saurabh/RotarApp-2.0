from django.shortcuts import render
from Auth.models import DistrictCouncil, Member, DistrictRole
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DistReport, Task, Response, Month
import json
from django.db import transaction
import datetime
import xlrd, xlwt
import pandas as pd
from django.db.models import IntegerField
from django.db.models.functions import Cast
from .decorators import is_DSA, is_council

@is_DSA
def admin_getMonth(request):
    if request.POST :
        file_name = request.FILES['files']
        file = pd.read_excel(file_name, sheet_name='Sheet1')
        del file['District Role']
        dictx = file.set_index('Role Id').T.to_dict(orient='list')
        month = Month.objects.filter(id=(request.POST['monthId'])).first()
        
        for row in dictx.keys():
            reportId = month.month+"-"+month.year+"-"+str(row)
            role = DistrictRole.objects.filter(distRoleId=str(row)).first()
            report, created = DistReport.objects.get_or_create(dReportId=reportId, month=month, districtRole = role)
            
            for text in dictx[row] :
                if(str(text)!='nan') :
                    
                    with transaction.atomic() :
                        newTask = Task(taskText=text)
                        newTask.save()
                    
                        newResponse = Response(dReport = report, task = newTask)
                        newResponse.save()

    months = Month.objects.filter(view=True).order_by('year','month').all()
    council = dict()
    roleList = DistrictRole.objects.filter(flag=True).annotate(id=Cast('distRoleId', IntegerField())).order_by('id').all()
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

    return render(request, 'DistReport/getMonth.html',{'title':'Tasks','Tab':'Tasks','DRole':'4','Council':council,'Months':months})

@is_DSA
def admin_getTasks(request, monthId, distRoleId):
    districtRole = DistrictRole.objects.filter(distRoleId=distRoleId).first()
    month = Month.objects.filter(id=monthId).first()
    reportId = month.month+"-"+month.year+"-"+str(districtRole.distRoleId)
    report, created = DistReport.objects.get_or_create(dReportId=reportId, month=month, districtRole=districtRole)
    response = Response.objects.filter(dReport=report).all().values_list('responseId','task__taskId','task__taskText','driveLink','completionStatus','response','modifiedOn','allottedBy')
    return render(request, 'DistReport/getTasks.html',{'title':'Tasks','Tab':'Tasks','DRole':'4','Response':response,'DistrictRole':districtRole,'ReportId':report.dReportId,'Month':month})

@is_DSA
def admin_manageAccess(request):
    months = Month.objects.all()
    return render(request, 'DistReport/monthPermissions.html',{'title':'Access','Tab':'Access','DRole':'4','Months':months})

@is_DSA
def admin_changePermission(request):
    data = json.loads(request.POST.get('data'))
    try :
        month = Month.objects.filter(id=data['monthId']).update(view=data['view'],edit=data['edit'])
        data = {
            'success': True
        }    

    except Exception as e :
        print(e)
        data = {
            'success': False
        }
    
    return JsonResponse(data)

@is_DSA
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

@is_DSA
def admin_deleteTask(request):
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
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
        print(Error)
        data = {
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }
        
    return JsonResponse(data)

@is_DSA
def admin_editTask(request):
    
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
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

@is_DSA
def admin_exportFormatFile(request):
    try :
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="'+'Tasks'+'.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        colwidth = int(30*260)

        ws = wb.add_sheet('Sheet1')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.alignment.wrap = 1
        columns = ['District Post','Role Id','Task 1','Task 2','Task 3','Task 4','Task 5','Task 6','Task 7','Task 8','Task 9','Task 10']
        for i in range(len(columns)):
            ws.col(i).width = colwidth
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        
        rows = DistrictRole.objects.filter(flag=True).annotate(id=Cast('distRoleId', IntegerField())).order_by('id').all().values_list('distRoleName','distRoleId')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)
        return response

    except Exception as e :
        print(e)
        response = None
        return response

@is_DSA
def admin_exportReports(request, monthId):
    try :
        response = HttpResponse(content_type='application/ms-excel')
        month = Month.objects.filter(id=monthId).first()
        Reports = DistReport.objects.filter(month=month).filter(districtRole__flag=True).annotate(id=Cast('districtRole__distRoleId', IntegerField())).order_by('id').all()
        response['Content-Disposition'] = 'attachment; filename="'+'Tasks'+"-"+str(month.month)+'-'+str(month.year)+'.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        colwidth = int(13*260)

        for Report in Reports :
            ws = wb.add_sheet(Report.districtRole.distRoleSName)
            row_num = 0
            font_style = xlwt.XFStyle()
            font_style.font.bold = True
            font_style.alignment.wrap = 1
            columns = ['Task','Status','Response','Drive Link','Assigned by','Last Modified']
            for i in range(len(columns)):
                ws.col(i).width = colwidth
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()
            font_style.alignment.wrap = 1
            rows = Response.objects.filter(dReport=Report).all().values_list('task__taskText','completionStatus','response','driveLink','allottedBy','modifiedOn')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)
        return response

    except Exception as e :
        print(e)
        response = None
        return response

@is_council
def council_index(request):
    months = Month.objects.filter(view=True).order_by('year','month').all()
    Council = DistrictCouncil.objects.filter(accountId = request.user).first()
    return render(request, 'DistReport/index.html',{'title':'Tasks','Tab':'Tasks','DRole':'1','DistRole':Council.districtRole.distRoleName,'Months':months})

@is_council
def council_getTasks(request):
    months = Month.objects.filter(view=True).order_by('year','month').all()   
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

    except Exception as Error :
        print(Error)
        data = {
            'success': False,
            'error' : "An error has occurred, Contact the website coordinators"
        }
        
    return JsonResponse(data)

@is_council
def council_saveTask(request):

    data = json.loads(request.POST.get('data'))
    
    task = data['data']

    try :
        
        response = Response.objects.filter(responseId = data['responseId'])
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

@is_council
def council_addTask(request):

    try :
        
        data = json.loads(request.POST.get('data'))
        
        Council = DistrictCouncil.objects.filter(accountId = request.user).first()

        month = Month.objects.filter(id=data['monthId']).first()
        reportId = month.month+"-"+month.year+"-"+str(Council.districtRole.distRoleId)

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

@is_council
def council_deleteTask(request):
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
            Response.objects.filter(responseId=data['responseId']).delete()

        Council = DistrictCouncil.objects.filter(accountId = request.user).first()

        report = DistReport.objects.filter(districtRole = Council.districtRole)
    
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

@is_council
def council_editTask(request):
    
    try :
        data = json.loads(request.POST.get('data'))
        
        with transaction.atomic() :
            Task.objects.filter(taskId=data['taskId']).update(taskText=data['taskText'])

        Council = DistrictCouncil.objects.filter(accountId = request.user).first()

        report = DistReport.objects.filter(districtRole = Council.districtRole)
    
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
        data = {
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }
        
    return JsonResponse(data)
