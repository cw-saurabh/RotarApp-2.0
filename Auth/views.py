from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileUpdateForm, EmailUpdateForm, AccountCreationForm
from .models import Club, Account, Member
from django.shortcuts import redirect
import csv
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseNotFound

def signup(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            Account = form.save()
            Account.refresh_from_db()
            member = Member.objects.create(login=Account,firstName=form.cleaned_data.get('firstName'),lastName=form.cleaned_data.get('lastName'))   
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=Account.username, password=raw_password)
            login(request, user)
            return redirect('main-home')
    else:
        form = AccountCreationForm()
    return render(request, 'Auth/signup.html', {'form': form,'title':'signup','Tab':'signup'})

# Create your views here.
@login_required
def updateClubProfile(request):

    clubProfile = Club.objects.filter(login=request.user).first()
    if request.user.loginType == '0' :
        edit = False
    else :
        edit = True
    return render(request, 'Auth/updateClubProfile.html',{'title':'Club Profile', 'Tab':'clubProfile', 'edit':edit, 'clubProfile':clubProfile})
    
    # if request.method == 'POST' :
    #     p_form = ProfileUpdateForm(request.POST, 
    #                                 request.FILES, 
    #                                 instance= Club.objects.filter(login=request.user).first())
    #     e_form = EmailUpdateForm(request.POST, instance=request.user)
    #     if e_form.is_valid():
    #         e_form.save()
    #     if p_form.is_valid():
    #         p_form.save()
    #     return redirect('profile')
    # else :
    #     p_form = ProfileUpdateForm(instance= Club.objects.filter(account=request.user).first())
    #     e_form = EmailUpdateForm(instance=request.user)

    # return render(request, 'Auth/updateProfile.html',{'title':'Profile','tab':'profile','pform':p_form,'eform':e_form,'profile':request.user.club})

@login_required
def updateUserProfile(request):
    profile = Member.objects.filter(login=request.user).first()
    if request.user.loginType == "1" :
        return HttpResponseNotFound("Page not found") 
    if request.method == 'POST' :
        p_form = UserProfileUpdateForm(request.POST or None, 
                                    request.FILES or None, 
                                    instance = Member.objects.filter(login=request.user).first())
        if p_form.is_valid():
            p_form.save()
        return redirect('updateUserProfile')
    else :
        p_form = UserProfileUpdateForm(instance = Member.objects.filter(login=request.user).first())
        
    return render(request, 'Auth/updateUserProfile.html',{'title':'Rotaractor','Tab':'userProfile','pform':p_form,'profile':profile,'edit':True,'club':'RC Panvel Central','clubRole':'Secretary','districtRole':'DES'})

@login_required
def viewUserProfile(request, username):
    user = Account.objects.filter(username=username).first()
    profile = Member.objects.filter(login=user).first()
    return render(request, 'Auth/updateUserProfile.html',{'title':'Rotaractor','Tab':'userProfile','profile':profile,'edit':False,'club':'RC Panvel Central','clubRole':'Secretary','districtRole':'DES'})

def createAccounts(request):
    csvFile='credentials.csv'
    with open(csvFile, encoding='utf8') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            try :
                p = Account(username=row['username'],
                name=row['Name2'],
                is_club = True,
                rotaryId = row['Club ID'])
                p.set_password(row['password'])
                p.save()

            except Exception as e:
                pass
                print(e)

    return redirect('login')

def email(request):
        try :
            subject = 'Testing'
            message = 'Thank you for being a part of this testing. Maine socha, time mila hai, benegit kar sakte hai, to mail ka feature add kar diya.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['pcpatil410@gmail.com','rtrmadhupimprikar@gmail.com']
            send_mail( subject, message, email_from, recipient_list )
            return redirect('home')
        except Exception as e: 
            print(e)