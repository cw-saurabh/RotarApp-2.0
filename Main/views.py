from django.shortcuts import render
from django.http import HttpResponse
from Auth.models import DistrictCouncil, Club
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

def zone(request):
    clubObjects = Club.objects.all()
    clubs = dict()
    zones = dict()    
    for club in clubObjects :
        if(club.zone and club.rotaryId and club.clubName!="") :
            clubs[club.rotaryId] = {
                    "clubId":club.rotaryId,
                    "clubLogo":club.clubLogo,
                    "clubName":club.clubName,
                    "charterDate":club.charterDate,
                    "about": club.clubName+"\nLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
                }
            if(club.zone) not in zones :
                zones[club.zone] = dict()    
            zones[club.zone][club.clubName] = {
                "clubId":club.rotaryId,
                "clubLogo":club.clubLogo,
                "clubName":club.clubName,
            }

    zones = [(k, v) for k, v in zones.items()] 
    zones = [tuple(zones[i:i+2]) for i in range(0, len(zones), 2)]

    return render(request, 'Main/m_zones.html',{'zones':zones,'clubs':clubs,'Tab':'zones'})

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]