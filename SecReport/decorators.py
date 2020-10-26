from django.core.exceptions import PermissionDenied
from Auth.models import Club, Account, DistrictCouncil
from .models import Report
from django.http import HttpResponseNotFound

def is_Club(function):
    def wrap(request, *args, **kwargs):
        admin = Account.objects.get(username='Superuser')
        if request.user == admin or request.user.loginType == '1':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseNotFound("Page not found") 
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def has_Access(function):

    # Allows admin and reporting club
    def wrap(request, *args, **kwargs):
        id = args[0] if args else kwargs['reportId']
        report = Report.objects.get(reportId=id)
        admin = Account.objects.get(username='Superuser')
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
        if request.user == admin or request.user == report.reportingClub.login or dRole=='44':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseNotFound("Page not found") 
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def is_DSR(function) :

    def wrap(request, *args, **kwargs):
        admin = Account.objects.get(username='Superuser')
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
        if request.user == admin or dRole == '44':
            return function(request, *args, **kwargs)
        else:
            print(dRole)
            print('Unauthorised')
            return HttpResponseNotFound("Access Restricted") 
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
