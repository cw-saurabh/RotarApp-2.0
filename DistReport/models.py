from django.db import models
from datetime import datetime, timedelta
from Auth.models import DistrictRole

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

class DistReport(models.Model):
    dReportId = models.CharField(blank = True, max_length=32, verbose_name = "Report Id", primary_key = True)
    reportingMonth = models.CharField(blank = True, max_length=2, choices = months, verbose_name = "Month")
    reportingYear = models.CharField(blank = True, max_length=4, verbose_name = "Year")
    districtRole = models.ForeignKey(DistrictRole, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'District Report'
        verbose_name_plural = 'District Reports'

    def __str__(self):
        return f'{self.districtRole.distRoleName}-{self.reportingMonth}'

class Task(models.Model) :
    taskId = models.AutoField(primary_key = True)
    taskText = models.CharField(blank = True, max_length = 100, verbose_name = 'Task')
    taskPoolStatus = models.BooleanField(verbose_name = "Task Pool Status", default = True, null = True, blank = True)

class Response(models.Model) :
    responseId = models.AutoField(primary_key=True)
    dReport = models.ForeignKey(DistReport, on_delete = models.CASCADE)
    task = models.ForeignKey(Task, on_delete = models.CASCADE)
    completionStatus = models.CharField(blank = True, max_length=2, choices = (("0","Incomplete"),("1","Partially Complete"),("2","Complete")), verbose_name = "Completion Status")
    response = models.TextField(blank = True, verbose_name = "Response")
    driveLink = models.CharField(blank = True, max_length = 100, verbose_name = "Drive Link")
    modifiedOn = models.DateTimeField(verbose_name = "Modified on", default=None, null = True, blank = True)
    allottedBy = models.CharField(blank = True, max_length=2, choices = (("0","DSA"),("1","Self")), verbose_name = "Allotted By", default='0')