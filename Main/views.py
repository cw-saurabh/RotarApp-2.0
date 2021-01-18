from django.shortcuts import render
from django.http import HttpResponse
from Auth.models import DistrictCouncil
from Main.models import WhatWeDo

# Create your views here.

def home(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/home.html',{'Tab':'home','DRole':dRole})

def home1(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/m_home.html',{'Tab':'home','DRole':dRole})

def aboutUs(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/m_aboutUs.html',{'Tab':'aboutUs','DRole':dRole})

def eRyla(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/m_eRyla.html',{'Tab':'aboutUs','DRole':dRole})

def council(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/m_council.html',{'Tab':'council','DRole':dRole})

def whatWeDo(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    events = WhatWeDo.objects.all()
    return render(request, 'Main/m_whatWeDo.html',{'Tab':'whatWeDo','DRole':dRole,'events':events})

def testWhatWeDo(request, eventId):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    event = WhatWeDo.objects.filter(id=eventId).first()
    return render(request, 'Main/m_testWhatWeDo.html',{'Tab':'whatWeDo','DRole':dRole,'event':event})

def resources(request):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/m_resources.html',{'Tab':'resources','DRole':dRole,'document':document})

def document(request,document):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    return render(request, 'Main/m_document.html',{'DRole':dRole,'document':document})
