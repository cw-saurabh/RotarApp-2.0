from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .models import Report, Meeting, Event, Bulletin, MemberMatrix, MemberMatrixAttribute, FeedbackQuestion, ReportBulletinMapping, ReportEventMapping, ReportMeetingMapping, Feedback, DuesPaid
from Auth.models import Club, Account
from datetime import datetime
import json
from django.forms.models import model_to_dict
from Main.models import FAQ
from django.db import transaction
import xlwt
from django.core.mail import send_mail
from django.conf import settings
from io import BytesIO
from django.core.mail import EmailMessage
from .decorators import is_Club, has_Access
import string
import random

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

    return redirect('login')

reportingMonth = str((datetime.now().month)-1) if ((datetime.now().month)-1)>9 else "0"+str((datetime.now().month)-1)
year = datetime.now().year

@login_required
@has_Access
def get_report(request,reportId,club):

    data = dict()
    report = Report.objects.filter(reportId=reportId).first()

    data = model_to_dict(report)

    data['ReportId'] = reportId
    data['ReportingMonth'] = report.reportingMonth
    data['DuesPaid'] = report.duesPaidAlready

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

    _club = Club.objects.filter(login=request.user).first()
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
                print(e)
                return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'danger':{'Message':'An error has occurred. Log in again and contact the website coordinators if the error retains.' }}})
              
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
            'error' : "An error has occurred, Contact the website coordinators",
            'success': False
        }

    return JsonResponse(data)

@login_required
@has_Access
def view_report(request,reportId) :
    _club = Club.objects.filter(login=request.user).first()
    report = Report.objects.filter(reportId=reportId)

    if report.exists() :
        data = get_report(request,reportId,_club)
        if report.first().status == '1' :
            return render(request, 'SecReport/reportView.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'Edit':False})
        else :
            return redirect('presentReport')
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
            return render(request, 'SecReport/response.html',{'Title':'Reporting','Tab':'Reporting','Messages':{'info':{'Message':'We have received your report for the previous month.'}},'ReportId':_reportId})
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
        return redirect('presentReport')
    except Exception as e:
        print(e)
        data = get_report(request, reportId,club)
        FAQs = FAQ.objects.all()
        return render(request, 'SecReport/report.html',{'Title':'Reporting','Tab':'Reporting','Report':data,'ClubProfile':club,'FAQs':FAQs,'Edit':False,'Error':'Submit failed, Contact website coordinators','Exception':e})

@login_required
@has_Access
def email_report(request,reportId):

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
            for col_num in range(5):
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
            for col_num in range(5):
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
    message = 'We have received your report for the previous month. Attaching it herewith.<br><br>For any queries, Contact - <br><br>Rtr. Prasad Seth (District Secretary - Reporting)<br>Call : +91 - 9623134392<br>Whatsapp : +91 - 9623134392<br>Mail Id: rtrprasadseth@gmail.com'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['rtrprasadseth@gmail.com']
    # send_mail( subject, message, email_from, recipient_list )


    message = EmailMessage(subject=subject, body=message,
        from_email=email_from,
        to=recipient_list)
    message.content_subtype = "html"
    filename=str(Club)+"-"+str(Month)+".xls"
    message.attach(filename, f.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") #get the stream and set the correct mimetype
    message.send()
    return redirect('main-home')

@login_required
@has_Access
def export_report(request,reportId):
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
            for col_num in range(5):
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
            for col_num in range(5):
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
