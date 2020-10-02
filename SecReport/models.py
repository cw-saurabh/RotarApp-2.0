from django.db import models
from Auth.models import Account, Club
import uuid
from datetime import datetime

months = (
    ("01","January"),
    ("02","February"),
    ("03","March"),
    ("04","April"),
    ("05","May"),
    ("06","June"),
    ("07","July"),
    ("08","August"),
    ("09","September"),
    ("10","October"),
    ("11","November"),
    ("12","December")
)

class DuesPaid(models.Model) :
    club = models.ForeignKey(Club, on_delete = models.CASCADE, null = True, blank = True)
    dues = models.IntegerField(blank = True, null = True, default = 0, verbose_name="Total Dues Paid")

    class Meta:
        verbose_name = 'Dues Paid'
        verbose_name_plural = 'Dues Paid'

    def __str__(self):
        return f'{self.club.clubName}-{self.dues}'


class Report(models.Model):
    reportId = models.CharField(blank = True, max_length=32, verbose_name = "Report Id", primary_key = True)
    reportingClub = models.ForeignKey(Club, on_delete = models.CASCADE, null = True, blank = True)
    reportingMonth = models.CharField(blank = True, max_length=2, choices = months, verbose_name = "Month")
    reportingDate = models.DateTimeField(verbose_name = "Reported on", default=datetime.now, null = True, blank = True)
    duesPaidAlready = models.CharField(blank = True, max_length=6, verbose_name = "District Dues paid upto the last month")
    duesPaidInThisMonth = models.CharField(blank = True, max_length=6,verbose_name = "District Dues paid in this month")
    suggestions = models.TextField(blank = True, max_length=1000,verbose_name = "Suggestions", default="")
    status = models.CharField(blank = True, max_length = 2, verbose_name = "Report Status", choices = (("0","Incomplete"),("1","Complete")), default = "0")

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return f'{self.reportingClub.clubName}-{self.reportingMonth}'


class MemberMatrixAttribute(models.Model):
    attribute = models.CharField(blank = True, max_length = 40, verbose_name = "Members Matrix Attribute")
    operation = models.CharField(blank = True, max_length=2, verbose_name ="Operation", default='')
    attributeStatus = models.BooleanField(verbose_name = "Status", default = True, null = True, blank = True)

    class Meta:
        verbose_name = 'MemberMatrixAttribute'
        verbose_name_plural = 'MemberMatrixAttributes'

    def __str__(self):
        return f'{self.attribute}'

class MemberMatrix(models.Model) :
    memberMatrixId = models.AutoField(primary_key=True)
    reportId = models.ForeignKey(Report, on_delete=models.CASCADE)
    attribute = models.ForeignKey(MemberMatrixAttribute, on_delete = models.CASCADE, null = True, blank = True)
    maleCount = models.CharField(blank = True, max_length=4,verbose_name = "Male Count")
    femaleCount = models.CharField(blank = True, max_length=4,verbose_name = "Female Count")
    othersCount = models.CharField(blank = True, max_length=4,verbose_name = "Others Count")

    class Meta:
        verbose_name = 'Member Matrix Row'
        verbose_name_plural = 'Member Matrix rows'

    def __str__(self):
        return f'{self.reportId.reportingClub.clubName}-{self.reportId.reportingMonth}-{self.attribute}'

class FeedbackQuestion(models.Model) :
    questionText = models.CharField(blank = True, max_length = 100, verbose_name = "Question Text")
    questionStatus = models.BooleanField(verbose_name = "Status", default = True, null = True, blank = True)

    class Meta:
        verbose_name = 'FeedbackQuestion'
        verbose_name_plural = 'FeedbackQuestions'

    def __str__(self):
        return f'{self.questionText}'

class Feedback(models.Model) :
    feedbackId = models.AutoField(primary_key=True)
    reportId = models.ForeignKey(Report, on_delete=models.CASCADE)
    feedbackQuestion = models.ForeignKey(FeedbackQuestion, on_delete = models.CASCADE, null = True, blank = True)
    booleanResponse = models.BooleanField(verbose_name = "Feedback Response", null = True, blank = True)

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return f'{self.reportId.reportingClub.clubName}-{self.reportId.reportingMonth}-{self.feedbackQuestion.id}'

class Meeting(models.Model) :
    meetingId = models.CharField(max_length=32, verbose_name = "Meeting Id", primary_key = True)
    hostClub = models.ForeignKey(Club, on_delete = models.CASCADE, null = True, blank = True, related_name = 'meeting')
    meetingNo = models.CharField(blank = True, verbose_name = "Meeting Number", default="", max_length = 3)
    meetingDate = models.DateTimeField(verbose_name = "Date", default=None, null = True, blank = True)
    meetingAgenda = models.CharField(blank = True, max_length=1000,verbose_name = "Agenda")
    bylawsBoolean = models.BooleanField(verbose_name="Bylaws passed?", null = True, blank = True)
    budgetBoolean = models.BooleanField(verbose_name="Budget passed?", null = True, blank = True)
    meetingAttendance = models.CharField(blank = True, max_length=5,verbose_name = "Attendance")
    meetingType = models.CharField(blank = True, max_length = 2, verbose_name = "Meeting Type", choices = (("1","BOD"),("2","GBM")))
    jointBoolean = models.BooleanField(default = False, verbose_name="is Joint?")

    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'

    def __str__(self):
        return f'{self.hostClub.clubName}-{self.meetingType}-{self.meetingDate.strftime("%d-%B")}' if self.meetingDate!=None else f'{self.hostClub.clubName}-{self.meetingType}'

class Event(models.Model):
    eventId = models.CharField(blank = True, max_length=32, verbose_name = "Event Id", primary_key = True)
    hostClub = models.ForeignKey(Club, on_delete = models.CASCADE, null = True, blank = True, related_name = 'event')
    eventStartDate = models.DateTimeField(verbose_name = "Start Date", null = True, blank = True)
    eventEndDate = models.DateTimeField(verbose_name = "End Date", null = True, blank = True)
    eventName = models.CharField(blank = True, max_length=50,verbose_name = "Name")
    eventAvenue = models.CharField(blank = True, max_length=5,verbose_name = "Avenue")
    eventAttendance = models.CharField(blank = True, max_length=6,verbose_name = "Attendance")
    eventHours = models.CharField(blank = True, max_length=6,verbose_name = "Volunteer Hours")
    eventFundRaised = models.CharField(blank = True, max_length=8,verbose_name = "Funds Raised")
    eventDescription = models.CharField(blank = True, max_length=1000,verbose_name = "Description")
    eventLink = models.CharField(blank = True, max_length=150,verbose_name = "Instagram Link")
    eventType = models.CharField(blank = True, max_length=2, verbose_name = "Event type", choices = (("1","Completed"),("2","Future Event")))
    jointBoolean = models.BooleanField(default = False, verbose_name="is Joint?")

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.eventName}-{self.hostClub.clubName}'
    
class Bulletin(models.Model) :
    bulletinId = models.CharField(blank = True, max_length=32, verbose_name = "Bulletin Id", primary_key = True)
    hostClub = models.ForeignKey(Club, on_delete = models.CASCADE, null = True, blank = True, related_name = 'Bulletin')
    bulletinName = models.CharField(blank = True, max_length=50,verbose_name = "Name of Bulletin")
    bulletinType = models.CharField(blank = True, max_length=10,verbose_name = "Type of Bulletin")
    bulletinLink = models.CharField(blank = True, max_length=150,verbose_name = "Link")
    bulletinIssuedOn = models.DateTimeField(verbose_name = "Issued on", null = True, blank = True)
    lastBulletinIssuedOn = models.DateTimeField(verbose_name = "Last Issued on", null = True, blank = True)
    bulletinFrequency = models.CharField(blank = True, max_length=20,verbose_name = "Frequency")
    jointBoolean = models.BooleanField(default = False, verbose_name="is Joint?")
    
    class Meta:
        verbose_name = 'Bulletin'
        verbose_name_plural = 'Bulletins'

    def __str__(self):
        return f'{self.bulletinId}-{self.hostClub.clubName}'

class ReportBulletinMapping(models.Model) :
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.bulletin.bulletinId}'

class ReportEventMapping(models.Model) :
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.report.reportingClub.clubName}-{self.report.reportingMonth}-{self.event.eventName}'

class ReportMeetingMapping(models.Model) :
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.report.reportingClub.clubName}-{self.report.reportingMonth}-{self.meeting.meetingType}-{self.meeting.meetingNo}'

class MeetingJointClubMapping(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    jointClub = models.ForeignKey(Club, on_delete=models.CASCADE)

class EventJointClubMapping(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    jointClub = models.ForeignKey(Club, on_delete=models.CASCADE)

class BulletinJointClubMapping(models.Model):
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    jointClub = models.ForeignKey(Club, on_delete=models.CASCADE)

class ReportViewPermission(models.Model) :
    club = models.ForeignKey(Club, on_delete = models.CASCADE, null = True, blank = True)
    hasPermission = models.BooleanField(default = False, verbose_name="Has permission?")