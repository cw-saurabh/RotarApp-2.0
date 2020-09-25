from django.shortcuts import render
from django.http import HttpResponse
from Auth.models import DistrictCouncil

# Create your views here.

def home(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
        print(dRole)
    return render(request, 'Main/home.html',{'Tab':'home','DRole':dRole})
