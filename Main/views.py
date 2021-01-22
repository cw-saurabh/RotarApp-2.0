from django.shortcuts import render
from django.http import HttpResponse
from Auth.models import DistrictCouncil
from Main.models import WhatWeDo, avenues
from django.http import HttpResponseNotFound

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

def whatWeDo(request, avenue = "0"):
    if avenue not in avenues.keys() :
        return HttpResponseNotFound("Page not found") 
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    events = WhatWeDo.objects.filter(eventCategory=str(avenue)).all()
    return render(request, 'Main/m_whatWeDo.html',{'Tab':'whatWeDo','SubTab':avenues[str(avenue)].replace(" ",''),'Header':avenues[str(avenue)],'DRole':dRole,'events':events})

def testWhatWeDo(request, eventId=-1):
    dRole = None
    if request.user.is_authenticated :
        dRole = DistrictCouncil.objects.filter(accountId = request.user).first()
        dRole = dRole.districtRole.distRoleId if dRole!=None else None
    events = WhatWeDo.objects.filter(id=eventId).all() if int(eventId)>=0 else WhatWeDo.objects.all()
    return render(request, 'Main/m_testWhatWeDo.html',{'Tab':'whatWeDo','DRole':dRole,'events':events})

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
