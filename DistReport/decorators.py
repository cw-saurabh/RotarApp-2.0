from django.core.exceptions import PermissionDenied
from Auth.models import Club, Account, DistrictCouncil
from django.http import HttpResponseNotFound

def is_DSA(function):
    def wrap(request, *args, **kwargs):
        admin = Account.objects.get(username='Superuser')
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
        if request.user == admin or dRole == '4':
            return function(request, *args, **kwargs)
        else:
            print(dRole)
            print('Unauthorised')
            return HttpResponseNotFound("Access Restricted") 
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def is_council(function):
    def wrap(request, *args, **kwargs):
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
        admin = Account.objects.get(username='Superuser')
        if request.user == admin or dRole!=None :
            return function(request, *args, **kwargs)
        else:
            print(dRole)
            print('Unauthorised')
            return HttpResponseNotFound("Access Restricted") 
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap