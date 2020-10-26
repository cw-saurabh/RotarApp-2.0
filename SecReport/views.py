from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Report, Meeting, Event, Bulletin, MemberMatrix, MemberMatrixAttribute, FeedbackQuestion, ReportBulletinMapping, ReportEventMapping, ReportMeetingMapping, Feedback, DuesPaid, Month, ReportAccess
from Auth.models import Club, Account, DistrictCouncil
from datetime import datetime
import json
from django.forms.models import model_to_dict
from Main.models import FAQ
from django.db import transaction, OperationalError
from django.db.models import IntegerField
from django.db.models.functions import Cast
import xlwt
from django.core.mail import send_mail
from django.conf import settings
from io import BytesIO
from django.core.mail import EmailMessage
from .decorators import is_Club, has_Access, is_DSR
import string
import random
import pandas as pd
from os import walk

class DeadlineMissed(Exception):
    pass

reportingMonth = str((datetime.now().month)-1) if ((datetime.now().month)-1)>9 else "0"+str((datetime.now().month)-1)
year = datetime.now().year

@login_required
@has_Access
def migrate_data(request):

    # p = FAQ(question='Where should we add PR Events ?',answer='Under Club Service')
    # p.save()
    # p = FAQ(question='Where should we add other avenue events ?',answer='Rotaract Events fall under 4 Categories : PD, ISD, CMD & CSD. If your event is under more than 2 avenues then add a new row and then add the same event again by just changing the avenue.')
    # p.save()
    # p = FAQ(question='What if we don\'t have an Instagram link or a drive link of a particular event/bulletin ?',answer='Just add a hyphen ( - )')
    # p.save()
    # p = FAQ(question='Which browsers are supported for Reporting ?',answer='You can use Chrome or Firefox Browser on mobile or desktop. Do not use Safari Browser.')
    # p.save()
    # p = FAQ(question='How can I save the data that I have filled ?',answer='Click on "Save" Button and your data will be saved.')
    # p.save()

    # p = MemberMatrixAttribute(attribute="Members at the beginning of this month")
    # p.save()
    # p = MemberMatrixAttribute(attribute="Members added")
    # p.save()
    # p = MemberMatrixAttribute(attribute="Members left")
    # p.save()
    # p = MemberMatrixAttribute(attribute="Prospective")
    # p.save()
    # p = MemberMatrixAttribute(attribute="Guests (RYE /NGSE /Family)")
    # p.save()

    # p = FeedbackQuestion(questionText="Whether you have received acknowledgement from the District Reporting Secretary ?")
    # p.save()
    # p = FeedbackQuestion(questionText="Do you get a prompt response from the DZR / AZR ?")
    # p.save()
    # p = FeedbackQuestion(questionText="Whether you have received receipt for payment of Dues ?")
    # p.save()
    # p = FeedbackQuestion(questionText="Do you get a timely response from the District ?")
    # p.save()

    return redirect('auth_login')

@login_required
@has_Access
def get_report(request,reportId,club):

    data = dict()
    report = Report.objects.filter(reportId=reportId).first()

    data = model_to_dict(report)

    data['ReportId'] = reportId
    data['ReportingMonth'] = report.reportingMonth
    data['DuesPaid'] = report.duesPaidAlready
    data['month'] = report.month.month
    data['year'] = report.month.year

    # GBM
    gbmData = {}
    gbmMappings = ReportMeetingMapping.objects.filter(report=reportId).filter( meeting__meetingType = "2").all().order_by('meeting__meetingNo')
    for gbmMapping in gbmMappings :
        gbmData[gbmMapping.meeting.meetingId]=model_to_dict(gbmMapping.meeting)
    data['GBMData'] = gbmData

    # BOD
    bodData = {}
    bodMappings = ReportMeetingMapping.objects.filter(report=reportId).filter( meeting__meetingType = "1").all().order_by('meeting__meetingNo')
    for bodMapping in bodMappings :
        bodData[bodMapping.meeting.meetingId]=model_to_dict(bodMapping.meeting)
    data['BODData'] = bodData

    # Matrix
    attributes = MemberMatrix.objects.filter(reportId=reportId).values('attribute__attribute','attribute__id','attribute__operation','maleCount','femaleCount','othersCount')
    data['MemberMatrix'] = attributes

    # Event
    eventData = {}
    eventMappings = ReportEventMapping.objects.filter(report=reportId).filter( event__eventType = "1").all().order_by('event__eventStartDate')
    for eventMapping in eventMappings :
        eventData[eventMapping.event.eventId]=model_to_dict(eventMapping.event)
    data['EventData'] = eventData

    # Bulletin
    bulletinMapping = ReportBulletinMapping.objects.filter(report=report).first()
    bulletin = model_to_dict(bulletinMapping.bulletin)
    data['Bulletin'] = bulletin

    # Future Event
    feventData = {}
    feventMappings = ReportEventMapping.objects.filter(report=reportId).filter( event__eventType = "2").all().order_by('event__eventStartDate')
    for feventMapping in feventMappings :
        feventData[feventMapping.event.eventId]=model_to_dict(feventMapping.event)
    data['FEventData'] = feventData

    # Feedback
    feedback = Feedback.objects.filter(reportId=reportId).values('feedbackQuestion__questionText','feedbackQuestion__id','booleanResponse')
    data['Questions'] = feedback

    return data

@login_required
@is_Club
def present_report(request):
    print(reportingMonth)
    _club = Club.objects.filter(login=request.user).all()
    _reportId = str(reportingMonth)+"-"+str(year)+"-"+str(request.user.username)
    report = Report.objects.filter(reportId=_reportId)

    if (True) : #Has permission
        FAQs = FAQ.objects.all()

        if report.exists() :
            data = get_report(request,_reportId,_club)
            if report.first().status == '1' :
                return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'info':{'Message':'We have received your report for the previous month.'}},'ReportId':_reportId})
            else :
                return render(request, 'SecReport/report.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'ClubProfile':_club,'FAQs':FAQs,'Edit':True})

        else :
            try :
                with transaction.atomic() :

                    newReport = Report(reportId=_reportId, reportingMonth=reportingMonth, reportingClub=_club, status = 0)
                    newReport.save()

                    salt = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 4))
                    bulletinId = "B-"+reportingMonth+"-"+salt
                    newBulletin = Bulletin(bulletinId=bulletinId,hostClub = _club)
                    newBulletin.save()
                    newBulletinMap = ReportBulletinMapping(report=newReport,bulletin=newBulletin)
                    newBulletinMap.save()

                    attributes = MemberMatrixAttribute.objects.all()
                    for attribute in attributes :
                        newMatrixRow = MemberMatrix(reportId = newReport, attribute=attribute)
                        newMatrixRow.save()

                    questions = FeedbackQuestion.objects.all()
                    for question in questions :
                        newFeedback = Feedback(reportId = newReport, feedbackQuestion=question)
                        newFeedback.save()

                    duesPaid = DuesPaid.objects.get(club=_club)
                    duesPaidAlreadyVar = duesPaid.dues
                    Report.objects.filter(reportId=_reportId).update(duesPaidAlready=duesPaidAlreadyVar)

                data = get_report(request,_reportId,_club)
                return render(request, 'SecReport/report.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'ClubProfile':club,'FAQs':FAQs,'Edit':True})

            except Exception as e :
                return redirect('presentReport')

    else :

        if report.exists() and report.first().status == '1' :
            return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'info':{'Message':'We have received your report for the previous month.'}},'ReportId':_reportId})
        else :
            return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'danger':{'Message':'The form is not accepting any response as of now.'}}})

@login_required
@has_Access
def upload_report(request, reportId, data, deletedData, status) :

    #Essentials
    club = Club.objects.filter(login=request.user).first()

    #Populate Dictionaries
    reportData = dict()
    for key in data.keys() :
        if not (type(data.get(key)) == dict) :
            reportData[key]=data.get(key)

    gbmsData = data['gbm'] if 'gbm' in data.keys() else None
    gbmsDeletedData = deletedData['gbm'] if 'gbm' in data.keys() else None

    bodsData = data['bod'] if 'bod' in data.keys() else None
    bodsDeletedData = deletedData['bod'] if 'bod' in data.keys() else None

    eventsData = data['event'] if 'event' in data.keys() else None
    eventsDeletedData = deletedData['event'] if 'event' in data.keys() else None

    feventsData = data['fevent'] if 'fevent' in data.keys() else None
    feventsDeletedData = deletedData['fevent'] if 'fevent' in data.keys() else None

    feedbackData = data['feedback'] if 'feedback' in data.keys() else None

    bulletinData = data['bulletin'] if 'bulletin' in data.keys() else None

    matrixData = data['matrix'] if 'matrix' in data.keys() else None

    incomingReport = Report.objects.filter(reportId=reportId)

    if incomingReport.exists() :
        print("Report exists")
        print(reportData)
        #Update Report
        incomingReport.update(**reportData)

        #Update meetings
        if gbmsData :
            for gbm in gbmsData.keys() :

                incomingGBM = Meeting.objects.filter(meetingId=gbm)

                if incomingGBM.exists():
                    print("GBM exists")
                    print(gbmsData[gbm])
                    incomingGBM.update(**gbmsData[gbm])
                else :
                    print("GBM created")
                    print(gbmsData[gbm])
                    with transaction.atomic() :
                        newGBM = Meeting(hostClub=club,meetingId=gbm,meetingType="2",**gbmsData[gbm])
                        newGBM.save()
                        newMap = ReportMeetingMapping(meeting = newGBM, report = incomingReport.first())
                        newMap.save()

        if gbmsDeletedData :
            for gbm in gbmsDeletedData:
                if Meeting.objects.filter(meetingId=gbm).exists() :
                    Meeting.objects.filter(meetingId=gbm).delete()

        if bodsData :
            for bod in bodsData.keys() :

                incomingBOD = Meeting.objects.filter(meetingId=bod)

                if incomingBOD.exists():
                    print("BOD exists")
                    print(bodsData[bod])
                    incomingBOD.update(**bodsData[bod])
                else :
                    print("BOD created")
                    print(bodsData[bod])
                    with transaction.atomic() :
                        newBOD = Meeting(hostClub=club,meetingId=bod,meetingType="1",**bodsData[bod])
                        newBOD.save()
                        newMap = ReportMeetingMapping(meeting = newBOD, report = incomingReport.first())
                        newMap.save()

        if bodsDeletedData :
            for bod in bodsDeletedData:
                if Meeting.objects.filter(meetingId=bod).exists() :
                    Meeting.objects.filter(meetingId=bod).delete()

        if eventsData :
            for event in eventsData.keys() :

                incomingEvent = Event.objects.filter(eventId=event)

                if incomingEvent.exists():
                    print("Event exists")
                    print(eventsData[event])
                    incomingEvent.update(**eventsData[event])
                else :
                    print("Event created")
                    print(eventsData[event])
                    with transaction.atomic() :
                        newEvent = Event(hostClub=club,eventId=event,eventType="1",**eventsData[event])
                        newEvent.save()
                        newMap = ReportEventMapping(event = newEvent, report = incomingReport.first())
                        newMap.save()

        if eventsDeletedData :
            for event in eventsDeletedData:
                if Event.objects.filter(eventId=event).exists() :
                    Event.objects.filter(eventId=event).delete()

        if feventsData :
            for fevent in feventsData.keys() :

                incomingFEvent = Event.objects.filter(eventId=fevent)

                if incomingFEvent.exists():
                    print("FEvent exists")
                    print(feventsData[fevent])
                    incomingFEvent.update(**feventsData[fevent])
                else :
                    print("FEvent created")
                    print(feventsData[fevent])
                    with transaction.atomic() :
                        newFEvent = Event(hostClub=club,eventId=fevent,eventType="2",**feventsData[fevent])
                        newFEvent.save()
                        newMap = ReportEventMapping(event = newFEvent, report = incomingReport.first())
                        newMap.save()

        if feventsDeletedData :
            for fevent in feventsDeletedData:
                if Event.objects.filter(eventId=fevent).exists() :
                    Event.objects.filter(eventId=fevent).delete()

        if feedbackData :
            print(feedbackData)
            for feedback in feedbackData :
                feedbackInstance = FeedbackQuestion.objects.get(id=feedback)
                incomingFeedback = Feedback.objects.filter(reportId=incomingReport.first(),feedbackQuestion=feedbackInstance)

                if incomingFeedback.exists():
                    print("Feedback exists")
                    incomingFeedback.update(**feedbackData[feedback])
                else :
                    raise Exception("Feedback object not found")

        if bulletinData :
            print(bulletinData)
            for bulletin in bulletinData :
                print(bulletin)
                incomingBulletin = Bulletin.objects.filter(bulletinId=bulletin)

                if incomingBulletin.exists() :
                    print("Bulletin exists")
                    incomingBulletin.update(**bulletinData[bulletin])
                else :
                    raise Exception("Bulletin object not found")

        if matrixData :
            print(matrixData)
            for attribute in matrixData :
                rowAttribute = MemberMatrixAttribute.objects.get(id=attribute)
                incomingRow = MemberMatrix.objects.filter(reportId=incomingReport.first(),attribute=rowAttribute)

                if incomingRow.exists():
                    print("Matrix Row exists")
                    incomingRow.update(**matrixData[attribute])
                else :
                    raise Exception("Member Matrix object not found")

    else :
        raise Exception("Report Object Not Found")

@login_required
def save_report(request) :
    data = json.loads(request.POST.get('data'))
    print(data)
    deletedData = json.loads(request.POST.get('deletedData'))
    reportId = data['reportId']

    try :
        upload_report(request, reportId, data, deletedData, 0)
        data = {
            'success': True
        }

    except Exception as Error :
        print(Error)
        data = {
            'error' : "The data has not been saved, make sure that the data you filled is emoji-free. DON'T REFRESH. Contact the website coordinators, if required.<br><br>",
            'success': False
        }

    return JsonResponse(data)

@login_required
@has_Access
def view_report(request,reportId) :
    
    report = Report.objects.filter(reportId=reportId)
    _club = report.first().reportingClub
    print(_club)

    if report.exists() :
        data = get_report(request,reportId,_club)
        if report.first().status == '1' :
            return render(request, 'SecReport/reportView.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'Edit':False,'profile':_club})
        else :
            return redirect('secReport_presentReport')
    else :
        return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'danger':{'Message':'Report not found. Contact the website coordinators if needed.' }}})

@login_required
@has_Access
def finish_report(request,reportId):
    club = Club.objects.filter(login=request.user).first()
    report = Report.objects.filter(reportId=reportId)
    FAQs = FAQ.objects.all()

    if report.exists() :
        data = get_report(request, reportId,club)
        if report.first().status == '1' :
            return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'info':{'Message':'We have received your report for the previous month.'}},'ReportId':reportId})
        else :
            return render(request, 'SecReport/reportView.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'Edit':True})
    else :
        return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'danger':{'Message':'Report not found. Contact the website coordinators if needed.' }}})

@login_required
@has_Access
def submit_report(request, reportId) :
    club = Club.objects.filter(login=request.user).first()
    try :
        with transaction.atomic() :
            report = Report.objects.filter(reportId=reportId)
            report.update(status="1")
            totalDues = DuesPaid.objects.get(club=club).dues
            duesPaidInThisMonth = report.first().duesPaidInThisMonth
            duesPaidAlready = report.first().duesPaidAlready
            totalDues = (0 if duesPaidAlready=='' else int(duesPaidAlready)) + (0 if duesPaidInThisMonth=='' else int(duesPaidInThisMonth))
            DuesPaid.objects.filter(club=club).update(dues=totalDues)

    except Exception as e:
        print(e)
        data = get_report(request, reportId,club)
        FAQs = FAQ.objects.all()
        return render(request, 'SecReport/report.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'ClubProfile':club,'FAQs':FAQs,'Edit':False,'Error':'Submit failed, Contact website coordinators','Exception':e})
    try :
        email_report(request, reportId)
    except Exception as e:
        print(e)
    return redirect('presentReport')

@login_required
@has_Access
def email_report(request,reportId):

    emailId = request.user.email
    print(emailId)
    Report1 = Report.objects.filter(reportId=reportId).all().first()
    Club = Report1.reportingClub.clubName
    Month = Report1.reportingMonth

    wb = xlwt.Workbook(encoding='utf-8')

    #Reports
    ws = wb.add_sheet('Reports')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.alignment.wrap = 1
    columns = ['Month','Date','Dues paid already','Dues paid in this month','Suggestions']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    rows = Report.objects.filter(reportId=reportId).all().values_list('reportingMonth','reportingDate','duesPaidAlready','duesPaidInThisMonth','suggestions')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    #GBM
    ws = wb.add_sheet('GBMs')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Meeting No.','Date','Agenda','Bylaws passed?','Budget passed?','Attendance']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    maps = ReportMeetingMapping.objects.filter(report=reportId,meeting__meetingType="2").all()
    for map in maps :
        row_num += 1
        rows = Meeting.objects.filter(meetingId=map.meeting.meetingId).all().values_list('meetingNo','meetingDate','meetingAgenda','bylawsBoolean','budgetBoolean','meetingAttendance')
        for row in rows :
            for col_num in range(6):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

    #BOD
    ws = wb.add_sheet('BODs')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Meeting No.','Date','Agenda','Bylaws passed?','Budget passed?','Attendance']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    maps = ReportMeetingMapping.objects.filter(report=reportId,meeting__meetingType="1").all()
    for map in maps :
        row_num += 1
        rows = Meeting.objects.filter(meetingId=map.meeting.meetingId).all().values_list('meetingNo','meetingDate','meetingAgenda','bylawsBoolean','budgetBoolean','meetingAttendance')
        for row in rows :
            for col_num in range(6):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

    #Events
    ws = wb.add_sheet('Events')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Event Name','Start Date','End Date','Avenue','Attendance','Voluntary Hours','Funds raised','Description','Link']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    maps = ReportEventMapping.objects.filter(report=reportId,event__eventType="1").all()
    for map in maps :
        row_num += 1
        rows = Event.objects.filter(eventId=map.event.eventId).all().values_list('eventName','eventStartDate','eventEndDate','eventAvenue','eventAttendance','eventHours','eventFundRaised','eventDescription','eventLink')
        for row in rows :
            for col_num in range(9):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

    #Future Events
    ws = wb.add_sheet('Future Events')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Event Name','Start Date','End Date','Avenue','Description']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    maps = ReportEventMapping.objects.filter(report=reportId,event__eventType="2").all()
    for map in maps :
        row_num += 1
        rows = Event.objects.filter(eventId=map.event.eventId).all().values_list('eventName','eventStartDate','eventEndDate','eventAvenue','eventDescription')
        for row in rows :
            for col_num in range(5):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

    #Feedback
    ws = wb.add_sheet('Feedback')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Question','Response']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = Feedback.objects.filter(reportId=reportId).all().values_list('feedbackQuestion__questionText','booleanResponse')
    for row in rows :
        row_num += 1
        for col_num in range(2):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    #Member Matrix
    ws = wb.add_sheet('Member Matrix')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Attribute', 'Male Count', 'Female Count', 'Others Count']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows = MemberMatrix.objects.filter(reportId=reportId).all().values_list('attribute__attribute','maleCount','femaleCount','othersCount')
    for row in rows :
        row_num += 1
        for col_num in range(4):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    #Bulletin
    ws = wb.add_sheet('Bulletin')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Bulletin Name','Bulletin Type','Bulletin Link','Issued on','Last bulletin Issued on','Frequency']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    maps = ReportBulletinMapping.objects.filter(report=reportId).all()
    for map in maps :
        row_num += 1
        rows = Bulletin.objects.filter(bulletinId=map.bulletin.bulletinId).all().values_list('bulletinName','bulletinType','bulletinLink','bulletinIssuedOn','lastBulletinIssuedOn','bulletinFrequency')
        for row in rows :
            for col_num in range(6):
                ws.write(row_num, col_num, str(row[col_num]), font_style)


    f = BytesIO() # create a file-like object
    wb.save(f)
    subject = 'Secretarial Report Received'
    message = 'We have received your report for the previous month. Find a copy of your report that has been attached herewith.<br><br>For any queries, Contact - <br><br>Rtr. Prasad Seth (District Secretary - Reporting)<br>Call : +91 - 9623134392<br>Whatsapp : +91 - 9623134392<br>Mail Id: rtrprasadseth@gmail.com'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['saurabh.s1999@gmail.com']
    recipient_list.append(emailId)
    # send_mail( subject, message, email_from, recipient_list )


    message = EmailMessage(subject=subject, body=message,
        from_email=email_from,
        to=recipient_list)
    message.content_subtype = "html"
    filename=str(Club)+"-"+str(Month)+".xls"
    message.attach(filename, f.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") #get the stream and set the correct mimetype
    message.send()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return HttpResponse(status=204)

@login_required
@has_Access
def export_report(request,reportId):
    try :
        response = HttpResponse(content_type='application/ms-excel')
        Report1 = Report.objects.filter(reportId=reportId).all().first()
        Club = Report1.reportingClub.clubName
        Month = Report1.reportingMonth
        response['Content-Disposition'] = 'attachment; filename="'+str(Club)+"-"+str(Month)+'.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        colwidth = int(13*260)

        #Reports
        ws = wb.add_sheet('Reports')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        font_style.alignment.wrap = 1
        columns = ['Month','Date','Dues paid already','Dues paid in this month','Suggestions']
        for i in range(len(columns)):
            ws.col(i).width = colwidth
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        rows = Report.objects.filter(reportId=reportId).all().values_list('reportingMonth','reportingDate','duesPaidAlready','duesPaidInThisMonth','suggestions')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        #GBM
        ws = wb.add_sheet('GBMs')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Meeting No.','Date','Agenda','Bylaws passed?','Budget passed?','Attendance']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        maps = ReportMeetingMapping.objects.filter(report=reportId,meeting__meetingType="2").all()
        for map in maps :
            row_num += 1
            rows = Meeting.objects.filter(meetingId=map.meeting.meetingId).all().values_list('meetingNo','meetingDate','meetingAgenda','bylawsBoolean','budgetBoolean','meetingAttendance')
            for row in rows :
                for col_num in range(6):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

        #BOD
        ws = wb.add_sheet('BODs')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Meeting No.','Date','Agenda','Bylaws passed?','Budget passed?','Attendance']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        maps = ReportMeetingMapping.objects.filter(report=reportId,meeting__meetingType="1").all()
        for map in maps :
            row_num += 1
            rows = Meeting.objects.filter(meetingId=map.meeting.meetingId).all().values_list('meetingNo','meetingDate','meetingAgenda','bylawsBoolean','budgetBoolean','meetingAttendance')
            for row in rows :
                for col_num in range(6):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

        #Events
        ws = wb.add_sheet('Events')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Event Name','Start Date','End Date','Avenue','Attendance','Voluntary Hours','Funds raised','Description','Link']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        maps = ReportEventMapping.objects.filter(report=reportId,event__eventType="1").all()
        for map in maps :
            row_num += 1
            rows = Event.objects.filter(eventId=map.event.eventId).all().values_list('eventName','eventStartDate','eventEndDate','eventAvenue','eventAttendance','eventHours','eventFundRaised','eventDescription','eventLink')
            for row in rows :
                for col_num in range(9):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

        #Future Events
        ws = wb.add_sheet('Future Events')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Event Name','Start Date','End Date','Avenue','Description']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        maps = ReportEventMapping.objects.filter(report=reportId,event__eventType="2").all()
        for map in maps :
            row_num += 1
            rows = Event.objects.filter(eventId=map.event.eventId).all().values_list('eventName','eventStartDate','eventEndDate','eventAvenue','eventDescription')
            for row in rows :
                for col_num in range(5):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)

        #Feedback
        ws = wb.add_sheet('Feedback')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Question','Response']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = Feedback.objects.filter(reportId=reportId).all().values_list('feedbackQuestion__questionText','booleanResponse')
        for row in rows :
            row_num += 1
            for col_num in range(2):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        #Member Matrix
        ws = wb.add_sheet('Member Matrix')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Attribute', 'Male Count', 'Female Count', 'Others Count']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        rows = MemberMatrix.objects.filter(reportId=reportId).all().values_list('attribute__attribute','maleCount','femaleCount','othersCount')
        for row in rows :
            row_num += 1
            for col_num in range(4):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        #Bulletin
        ws = wb.add_sheet('Bulletin')
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Bulletin Name','Bulletin Type','Bulletin Link','Issued on','Last bulletin Issued on','Frequency']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        font_style = xlwt.XFStyle()
        maps = ReportBulletinMapping.objects.filter(report=reportId).all()
        for map in maps :
            row_num += 1
            rows = Bulletin.objects.filter(bulletinId=map.bulletin.bulletinId).all().values_list('bulletinName','bulletinType','bulletinLink','bulletinIssuedOn','lastBulletinIssuedOn','bulletinFrequency')
            for row in rows :
                for col_num in range(6):
                    ws.write(row_num, col_num, str(row[col_num]), font_style)


        wb.save(response)
        return response

    except Exception as e :
        response = None
        return response

@login_required
@has_Access
def load_reports(request): #July Only
    print("Hii")
    f = []
    for (dirpath, dirnames, filenames) in walk('.\SecReport - August'):
        f.extend(filenames)
        break

    for filename in f :
        _clubname, _year, _month = filename.split('-')[0], filename.split('-')[1], filename.split('-')[2].split('.')[0]
        _reportId = str(_month)+"-"+str(_year)+"-"+str(_clubname)
        
        clubAccount = Account.objects.filter(username=_clubname).first()
        club = Club.objects.filter(login=clubAccount).first()

        #report object
        report_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='Reports')
        report_dictx = report_file.set_index('Month').T.to_dict(orient='list')
        date = report_dictx['2020-07'][0]
        duesPaidAlready = report_dictx['2020-07'][1]
        duesPaidInThisMonth = report_dictx['2020-07'][2]
        suggestions = report_dictx['2020-07'][3]
        
        report = Report.objects.filter(reportId=_reportId)
        if report.exists() :
            report.update(reportId=_reportId,reportingClub=club,reportingMonth=_month,reportingDate=date,duesPaidAlready=duesPaidAlready,duesPaidInThisMonth=duesPaidInThisMonth,suggestions=suggestions,status='1')
        else :
            report = Report(reportId=_reportId,reportingClub=club,reportingMonth=_month,reportingDate=date,duesPaidAlready=duesPaidAlready,duesPaidInThisMonth=duesPaidInThisMonth,suggestions=suggestions,status='1')
            report.save()
        
        report = Report.objects.filter(reportId=_reportId)
        
        # gbm object
        gbm_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='GBMs')
        gbm_dictx = gbm_file.set_index('Meeting No.').T.to_dict(orient='list')
        gbmsData = dict()
        for gbm in gbm_dictx.keys() :
            gbmId = 'M-' + str(gbm) + '-' + _month + ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
            gbmsData[gbmId] = {
                'meetingNo' : gbm,
                'meetingDate' : gbm_dictx[gbm][0] if gbm_dictx[gbm][0]!='None' else None,
                'meetingAgenda' : gbm_dictx[gbm][1],
                'bylawsBoolean' : gbm_dictx[gbm][2],
                'budgetBoolean' : gbm_dictx[gbm][3],
                'meetingAttendance' : gbm_dictx[gbm][4]
            }
            incomingGBM = Meeting.objects.filter(meetingId=gbmId)
            if incomingGBM.exists():
                incomingGBM.update(**gbmsData[gbmId])
            else :
                with transaction.atomic() :
                    newGBM = Meeting(hostClub=club,meetingId=gbmId,meetingType="2",**gbmsData[gbmId])
                    newGBM.save()
                    newMap = ReportMeetingMapping(meeting = newGBM, report = report.first())
                    newMap.save()

        # BOD object
        bod_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='BODs')
        bod_dictx = bod_file.set_index('Meeting No.').T.to_dict(orient='list')
        bodsData = dict()
        for bod in bod_dictx.keys() :
            bodId = 'M-' + str(bod) + '-' + _month + ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
            bodsData[bodId] = {
                'meetingNo' : bod,
                'meetingDate' : bod_dictx[bod][0] if bod_dictx[bod][0]!='None' else None,
                'meetingAgenda' : bod_dictx[bod][1],
                'bylawsBoolean' : bod_dictx[bod][2],
                'budgetBoolean' : bod_dictx[bod][3],
                'meetingAttendance' : bod_dictx[bod][4],
            }
            incomingBOD = Meeting.objects.filter(meetingId=bodId)
            if incomingBOD.exists():
                incomingBOD.update(**bodsData[bodId])
            else :
                with transaction.atomic() :
                    newBOD = Meeting(hostClub=club,meetingId=bodId,meetingType="1",**bodsData[bodId])
                    newBOD.save()
                    newMap = ReportMeetingMapping(meeting = newBOD, report = report.first())
                    newMap.save()

        # event object
        event_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='Events')
        event_dictx = event_file.set_index('Name').T.to_dict(orient='list')
        eventsData = dict()
        eventCounter = 0

        for eventName in event_dictx.keys() :
            eventId = 'E-' + str(eventCounter) + '-' + _month + ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
            eventCounter+=1
            eventsData[eventId] = {
                'eventName' : eventName,
                'eventStartDate' : event_dictx[eventName][0] if event_dictx[eventName][0]!='None' else None,
                'eventEndDate' : event_dictx[eventName][1] if event_dictx[eventName][1]!='None' else None,
                'eventAvenue' : event_dictx[eventName][2],
                'eventAttendance' : event_dictx[eventName][3],
                'eventHours' : event_dictx[eventName][4],
                'eventFundRaised' : event_dictx[eventName][5],
                'eventDescription' : event_dictx[eventName][6],
                'eventLink' : event_dictx[eventName][7],
            }
            incomingEvent = Event.objects.filter(eventId=eventId)

            if incomingEvent.exists():
                incomingEvent.update(**eventsData[eventId])
            else :
                with transaction.atomic() :
                    newEvent = Event(hostClub=club,eventId=eventId,eventType="1",**eventsData[eventId])
                    newEvent.save()
                    newMap = ReportEventMapping(event = newEvent, report = report.first())
                    newMap.save()

        # fevent object
        fevent_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='Future Events')
        fevent_dictx = fevent_file.set_index('Event Name').T.to_dict(orient='list')
        feventsData = dict()
        feventCounter = 0

        for feventName in fevent_dictx.keys() :
            feventId = 'E-' + str(feventCounter) + '-' + _month + ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
            feventCounter+=1
            feventsData[feventId] = {
                'eventName' : feventName,
                'eventStartDate' : fevent_dictx[feventName][0] if fevent_dictx[feventName][0]!='None' else None,
                'eventEndDate' : fevent_dictx[feventName][1] if fevent_dictx[feventName][1]!='None' else None,
                'eventAvenue' : fevent_dictx[feventName][2],
                'eventDescription' : fevent_dictx[feventName][3],
            }
            incomingFEvent = Event.objects.filter(eventId=feventId)

            if incomingFEvent.exists():
                incomingFEvent.update(**feventsData[feventId])
            else :
                with transaction.atomic() :
                    newFEvent = Event(hostClub=club,eventId=feventId,eventType="2",**feventsData[feventId])
                    newFEvent.save()
                    newMap = ReportEventMapping(event = newFEvent, report = report.first())
                    newMap.save()

        # Bulletin object
        bulletin_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='Bulletin')
        bulletin_dictx = bulletin_file.set_index('Bulletin Name').T.to_dict(orient='list')
        bulletinData = dict()
        bulletinCounter = 0
        for bulletinName in bulletin_dictx.keys() :
            bulletinId = 'B-' + str(bulletinCounter) + '-' + _month + '-' + ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 5))
            bulletinCounter+=1
            bulletinData[bulletinId] = {
                'bulletinName' : bulletinName,
                'bulletinIssuedOn' : bulletin_dictx[bulletinName][2] if bulletin_dictx[bulletinName][2]!='None' else None,
                'lastBulletinIssuedOn' : bulletin_dictx[bulletinName][3] if bulletin_dictx[bulletinName][3]!='None' else None,
                'bulletinType' : bulletin_dictx[bulletinName][0],
                'bulletinLink' : bulletin_dictx[bulletinName][1],
                'bulletinFrequency' : bulletin_dictx[bulletinName][4],
            }
            with transaction.atomic() :
                newBulletin = Bulletin(bulletinId=bulletinId, hostClub = club, **bulletinData[bulletinId])
                newBulletin.save()
                newBulletinMap = ReportBulletinMapping(report=report.first(),bulletin=newBulletin)
                newBulletinMap.save()

        # Feedback object
        feedback_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='Feedback')
        feedback_dictx = feedback_file.set_index('Question').T.to_dict(orient='list')

        for feedback in feedback_dictx.keys() :
            feedbackInstance = FeedbackQuestion.objects.filter(questionText=feedback).first()
            incomingFeedback = Feedback(reportId=report.first(),feedbackQuestion=feedbackInstance, booleanResponse = feedback_dictx[feedback][0])
            incomingFeedback.save()

        # Member matrix object
        matrix_file = pd.read_excel(".\SecReport - August\\"+filename, sheet_name='Member Matrix')
        matrix_dictx = matrix_file.set_index('Attribute').T.to_dict(orient='list')
        for attribute in matrix_dictx.keys() :
            attributeInstance = MemberMatrixAttribute.objects.filter(attribute=attribute).first()
            incomingMatrix = MemberMatrix(reportId=report.first(),attribute=attributeInstance, maleCount = matrix_dictx[attribute][0], femaleCount = matrix_dictx[attribute][1], othersCount = matrix_dictx[attribute][2])
            incomingMatrix.save()
        
    return redirect('auth_login')

# New format
    
@login_required 
@is_Club
def add_month(request) :
    reports = Report.objects.all()
    for report in reports :
        month = Month.objects.filter(month=report.reportingMonth).first()
        report.month = month
        print(month)
        print(report.month)
        report.save()

@login_required
@is_Club
def createMonths(request) :
    Month(year='2020',month='01').save()
    Month(year='2020',month='02').save()
    Month(year='2020',month='03').save()
    Month(year='2020',month='04').save()
    Month(year='2020',month='05').save()
    Month(year='2020',month='06').save()
    Month(year='2020',month='07').save()
    Month(year='2020',month='08').save()
    Month(year='2020',month='09').save()
    Month(year='2020',month='10').save()
    Month(year='2020',month='11').save()
    Month(year='2020',month='12').save()

@login_required
@is_Club
def createPermissions(request):
    clubs = Club.objects.all()
    months = Month.objects.all()
    for club in clubs :
        for month in months :
            ReportAccess(club=club, month=month).save()
    return HttpResponseNotFound('Ho gaya bhai')

@login_required
@has_Access
def get_report1(request,reportId,club):

    data = dict()
    report = Report.objects.filter(reportId=reportId).first()

    data = model_to_dict(report)

    data['ReportId'] = reportId
    data['ReportingMonth'] = report.reportingMonth
    data['DuesPaid'] = report.duesPaidAlready
    print(report.duesPaidAlready)
    data['status'] = report.status

    # GBM
    gbmData = {}
    gbmMappings = ReportMeetingMapping.objects.filter(report=reportId).filter( meeting__meetingType = "2").all().order_by('meeting__meetingNo')
    for gbmMapping in gbmMappings :
        gbmData[gbmMapping.meeting.meetingId]=model_to_dict(gbmMapping.meeting)
    data['GBMData'] = gbmData

    # BOD
    bodData = {}
    bodMappings = ReportMeetingMapping.objects.filter(report=reportId).filter( meeting__meetingType = "1").all().order_by('meeting__meetingNo')
    for bodMapping in bodMappings :
        bodData[bodMapping.meeting.meetingId]=model_to_dict(bodMapping.meeting)
    data['BODData'] = bodData

    # Matrix
    attributes = MemberMatrix.objects.filter(reportId=reportId).values('attribute__attribute','attribute__id','attribute__operation','maleCount','femaleCount','othersCount')
    data['MemberMatrix'] = list(attributes)

    # Event
    eventData = {}
    eventMappings = ReportEventMapping.objects.filter(report=reportId).filter( event__eventType = "1").all().order_by('event__eventStartDate')
    for eventMapping in eventMappings :
        eventData[eventMapping.event.eventId]=model_to_dict(eventMapping.event)
    data['EventData'] = eventData

    # Bulletin
    bulletinMapping = ReportBulletinMapping.objects.filter(report=report).first()
    bulletin = model_to_dict(bulletinMapping.bulletin)
    data['Bulletin'] = bulletin

    # Future Event
    feventData = {}
    feventMappings = ReportEventMapping.objects.filter(report=reportId).filter( event__eventType = "2").all().order_by('event__eventStartDate')
    for feventMapping in feventMappings :
        feventData[feventMapping.event.eventId]=model_to_dict(feventMapping.event)
    data['FEventData'] = feventData

    # Feedback
    feedback = Feedback.objects.filter(reportId=reportId).values('feedbackQuestion__questionText','feedbackQuestion__id','booleanResponse')
    data['Questions'] = list(feedback)

    return data

@login_required
@is_Club
def present_report1(request) :
    FAQs = FAQ.objects.all()
    club = Club.objects.filter(login=request.user).first()
    months = ReportAccess.objects.filter(club=club).filter(view=True).order_by('month__year','month__month').values('month__id','month__month','month__year','edit').all()
    return render(request, 'SecReport/secReport.html',{'Title':'Reporting','Tab':'Reporting','Months':months,'profile':club,'FAQs':FAQs})

@login_required
@is_Club
def fetch_reports(request) :
    club = Club.objects.filter(login=request.user).first()
    months = ReportAccess.objects.filter(club=club).filter(view=True).order_by('month__year','month__month').values('month__id','month__month','month__year','edit').all()
    
    response = {'success':True}
    months_dictx = {}

    for month in months :
        months_dictx[month['month__id']] = {}
        monthObject = Month.objects.filter(id=month['month__id']).first()
        _reportId = str(month['month__month'])+"-"+str(month['month__year'])+"-"+str(request.user.username)

        report = Report.objects.filter(reportId=_reportId)
        if report.exists() :
            months_dictx[month['month__id']] = get_report1(request, _reportId, club)
            print("Report exists")
        else :
            try :
                with transaction.atomic() :

                    newReport = Report(reportId=_reportId, month=monthObject, reportingClub=club, status = 0)
                    newReport.save()

                    salt = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = 4))
                    bulletinId = "B-"+reportingMonth+"-"+salt
                    newBulletin = Bulletin(bulletinId=bulletinId,hostClub = club)
                    newBulletin.save()
                    newBulletinMap = ReportBulletinMapping(report=newReport,bulletin=newBulletin)
                    newBulletinMap.save()

                    attributes = MemberMatrixAttribute.objects.all()
                    for attribute in attributes :
                        newMatrixRow = MemberMatrix(reportId = newReport, attribute=attribute)
                        newMatrixRow.save()

                    questions = FeedbackQuestion.objects.all()
                    for question in questions :
                        newFeedback = Feedback(reportId = newReport, feedbackQuestion=question)
                        newFeedback.save()

                    duesPaid = DuesPaid.objects.get(club=club)
                    duesPaidAlreadyVar = duesPaid.dues
                    Report.objects.filter(reportId=_reportId).update(duesPaidAlready=duesPaidAlreadyVar)

                months_dictx[month['month__id']] = get_report1(request, _reportId, club)
                print("Report created")


            except Exception as e :
                print(e)
                response = {'success':False}

    response['data'] = months_dictx
            
    
    return JsonResponse(response)

@login_required
def save_report1(request) :

    data = json.loads(request.POST.get('data'))
    deletedData = json.loads(request.POST.get('deletedData'))
    reportId = request.POST.get('reportId')
    report = Report.objects.filter(reportId=reportId).first()
    club = Club.objects.filter(login=request.user).first()

    try :
        permission = ReportAccess.objects.filter(club=club).filter(month=report.month).first()
        if permission.edit :
            upload_report(request, reportId, data, deletedData, 0)
            data = {
                'success': True
            }
        else :
            raise DeadlineMissed
        
    except DeadlineMissed as Error :
        print(Error)
        print(type(Error).__name__)
        data = {
            'error' : "You missed the deadline. <br>Contact District Reporting Secretary, if required.<br><br>",
            'success': False
        }

    except OperationalError as Error :
        print(Error)
        print(type(Error).__name__)
        data = {
            'error' : "The data has not been saved, make sure that the data you filled is emoji-free. DON'T REFRESH.<br>Contact the website coordinators, if required.<br><br>",
            'success': False
        }

    except Exception as Error :
        print(Error)
        print(type(Error).__name__)
        data = {
            'error' : "The data has not been saved. Do not refresh the browser.<br>Contact the website coordinators, if required.<br><br>",
            'success': False
        }

    return JsonResponse(data)

@login_required
def finish_report1(request) :

    reportId = request.POST.get('reportId')
    report = Report.objects.filter(reportId=reportId).first()

    try :
        report = Report.objects.filter(reportId=reportId)
        report.update(status="2")
        
        data = {
            'success':True
        }
    except Exception as Error :
        print(Error)
        print(type(Error).__name__)
        data = {
            'error' : "An error has occurred. <br>Contact the website coordinators, if required.<br><br>",
            'success': False
        }

    return JsonResponse(data)

@login_required
def edit_report1(request) :

    reportId = request.POST.get('reportId')
    report = Report.objects.filter(reportId=reportId).first()

    try :
        report = Report.objects.filter(reportId=reportId)
        report.update(status="0")
        
        data = {
            'success':True
        }
        
    except Exception as Error :
        print(Error)
        print(type(Error).__name__)
        data = {
            'error' : "An error has occurred. <br>Contact the website coordinators, if required.<br><br>",
            'success': False
        }

    return JsonResponse(data)

@login_required
def submit_report1(request) :

    reportId = request.POST.get('reportId')
    report = Report.objects.filter(reportId=reportId).first()

    try :

        club = Club.objects.filter(login=request.user).first()

        with transaction.atomic() :
            report = Report.objects.filter(reportId=reportId)
            report.update(status="1")
            totalDues = DuesPaid.objects.get(club=club).dues
            duesPaidInThisMonth = report.first().duesPaidInThisMonth
            duesPaidAlready = report.first().duesPaidAlready
            totalDues = (0 if duesPaidAlready=='' else int(duesPaidAlready)) + (0 if duesPaidInThisMonth=='' else int(duesPaidInThisMonth))
            DuesPaid.objects.filter(club=club).update(dues=totalDues)


        data = {
            'success':True
        }

    except Exception as Error :
        print(Error)
        print(type(Error).__name__)
        data = {
            'error' : "An error has occurred. <br>Contact the website coordinators, if required.<br><br>",
            'success': False
        }

    return JsonResponse(data)


@login_required
@is_DSR
def manageAccess(request) :
    dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
    dRole = dRole.districtRole.distRoleId if dRole!=None else None
    months = Month.objects.order_by('year','month').all()
    return render(request,'SecReport/admin_manageAccess.html',{'Months':months,'Title':'Manage Access','Tab':'s_access','DRole':dRole})

@login_required
@is_DSR
def getPermissions(request) :
    
    response = {}

    try :
        months = Month.objects.order_by('year','month').all()
        permissions = dict()
        for month in months :
            row = ReportAccess.objects.filter(month=month).values('id','month__id','club__clubName','edit','view')
            permissions[month.id] = list(row)
        
        response['success'] = True
        response['data'] = permissions

    except Exception as e :
        print(e)
        response['success'] = False
        response['data'] = None

    return JsonResponse(response)

@login_required
@is_DSR
def changePermission(request):
    data = json.loads(request.POST.get('data'))
    try :
        if data['permissionId']=='all' :
            permission = ReportAccess.objects.filter(month__id=data['monthId']).update(view=data['view'],edit=data['edit'])
        else :
            permission = ReportAccess.objects.filter(id=data['permissionId']).update(view=data['view'],edit=data['edit'])
        data = {
            'success': True
        }

    except Exception as e :
        print(e)
        data = {
            'success': False
        }

    return JsonResponse(data)

@login_required
@is_DSR
def responses(request) :
    dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
    dRole = dRole.districtRole.distRoleId if dRole!=None else None
    months = Month.objects.order_by('year','month').all()
    reports = dict()
    for month in months :
        reports[month.id] = list(Report.objects.filter(month=month).annotate(intStatus=Cast('status', IntegerField())).order_by('-intStatus').values('status','reportId','reportingClub__clubName','reportingClub__clubLogo','duesPaidInThisMonth','suggestions'))
        
    return render(request,'SecReport/admin_responses.html',{'Months':months,'Title':'Reports','Tab':'s_responses','DRole':dRole,'Reports':reports})
