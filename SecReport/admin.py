from django.contrib import admin
from .models import DuesPaid, ReportViewPermission, Report, Meeting, Event, Bulletin, MemberMatrix, MemberMatrixAttribute, FeedbackQuestion, Feedback, ReportBulletinMapping, ReportEventMapping, ReportMeetingMapping, MeetingJointClubMapping, BulletinJointClubMapping, EventJointClubMapping

# Register your models here.

class ReportAdmin(admin.ModelAdmin):
    verbose_name_plural = "Reports"
    list_display = ['reportingClub','reportingMonth','status','suggestions' ]


admin.site.register(Report, ReportAdmin)
admin.site.register(Meeting)
admin.site.register(Event)
admin.site.register(Bulletin)
admin.site.register(MemberMatrix)
admin.site.register(MemberMatrixAttribute)
admin.site.register(FeedbackQuestion)
admin.site.register(Feedback)
admin.site.register(DuesPaid)
admin.site.register(ReportViewPermission)

admin.site.register(ReportMeetingMapping)
admin.site.register(ReportEventMapping)
admin.site.register(ReportBulletinMapping)

# admin.site.register(EventJointClubMapping)
# admin.site.register(BulletinJointClubMapping)
# admin.site.register(MeetingJointClubMapping)

