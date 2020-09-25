
from django.db import models
import uuid
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta

loginTypes = (
    ("0", "Rotaractor"),
    ("1", "Admin")
)

class Account(AbstractUser):
    loginId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = None
    last_name = None
    date_joined = None
    loginType = models.CharField(
        max_length = 2,
        choices = loginTypes,
        default = '0'
        )
    email = models.EmailField(blank=False)
    REQUIRED_FIELDS = ['loginType','email']

    def __str__(self):
        return (self.username)

    class Meta:
        verbose_name = 'Username'
        verbose_name_plural = 'Usernames'

class District(models.Model):
    distId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    distName = models.CharField(verbose_name = "District Id", max_length = 5, blank=True, null=True)
    distLogo = models.ImageField(verbose_name="District Logo", upload_to="distLogos")

    def __str__(self):
        return f'{self.distName}'

    class Meta:
        verbose_name = 'District'
        verbose_name_plural = 'Districts'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        try :
            img = Image.open(self.distLogo.path)
            width = img.size[0]

            if width > 720 :
                width = 720
                wpercent = (width/float(img.size[0]))
                height = int((float(img.size[1])*float(wpercent)))
                img = img.resize((width,height), Image.ANTIALIAS)
                img.save(self.distLogo.path)
        except Exception as e:
            print(e)

class Club(models.Model):
    clubId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.OneToOneField(Account, on_delete=models.CASCADE)
    clubName = models.CharField(max_length=50,verbose_name = "Name", default="",blank=True)
    zone = models.CharField(verbose_name = "Zone", max_length = 2, blank=True, null=True)
    clubLogo = models.ImageField(verbose_name="Club Logo", upload_to="clubLogos")
    charterDate  = models.DateTimeField(verbose_name = "Charter Date", null=True, blank=True, default=None)
    meetingPlace = models.CharField(max_length=100,verbose_name = "Meeting Place", null=True, blank=True, default=None)
    rotaryId = models.CharField(max_length=7, verbose_name = "Rotary Id", null=True, blank=True, default="")

    def __str__(self):
        return f'{self.clubName}'

    class Meta:
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'

    def save(self, *args, **kwargs):
        try:
            this = Club.objects.get(clubId=self.clubId)
            if this.clubLogo.path != self.clubLogo.path :
                this.clubLogo.delete()
        except Exception as e:
            print(e)

        super().save(*args, **kwargs)

        try :
            img = Image.open(self.clubLogo.path)
            width = img.size[0]

            if width > 720 :
                width = 720
                wpercent = (width/float(img.size[0]))
                height = int((float(img.size[1])*float(wpercent)))
                img = img.resize((width,height), Image.ANTIALIAS)
                img.save(self.clubLogo.path)
        except Exception as e:
            print(e)

class Member(models.Model):
    memberId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.OneToOneField(Account, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=15,verbose_name = "First Name", default="",blank=True)
    lastName = models.CharField(max_length=15,verbose_name = "Last Name", default="",blank=True, null=True)
    gender = models.CharField(
        max_length = 1,
        choices = (("M","Male"),("F","Female"),("O","Others")),
        default = None,
        blank = True,
        null = True
        )
    rotaryId = models.IntegerField(verbose_name = "Rotary Id",null=True,blank=True)
    contact = models.CharField(max_length=10,verbose_name = "Contact Number", default="",blank=True, null=True)
    birthDate = models.DateTimeField(verbose_name = "Birth Date", null=True, blank=True, default=None)
    bloodGroup = models.CharField(max_length=3,verbose_name = "Blood Group", default=None,blank=True, null=True)
    photo = models.ImageField(verbose_name="Photo", upload_to="profilePics", null=True)
    joiningDate = models.DateTimeField(verbose_name = "Joining Date", null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.firstName}'

    class Meta:
        verbose_name = 'Rotaractor'
        verbose_name_plural = 'Rotaractors'

    def save(self, *args, **kwargs):
        try:
            this = Member.objects.get(memberId=self.memberId)
            if this.photo.path != self.photo.path :
                this.photo.delete()
        except Exception as e:
            print(e)

        super().save(*args, **kwargs)

        try :
            img = Image.open(self.photo.path)
            width = img.size[0]

            if width > 720 :
                width = 720
                wpercent = (width/float(img.size[0]))
                height = int((float(img.size[1])*float(wpercent)))
                img = img.resize((width,height), Image.ANTIALIAS)
                img.save(self.photo.path)
        except Exception as e:
            print(e)

class ClubRole(models.Model):
    clubRoleId = models.AutoField(primary_key=True)
    clubRoleName = models.CharField(max_length=15,verbose_name = "Club Role Name")

    def __str__(self):
        return f'{self.clubRoleName}'

    class Meta:
        verbose_name = 'Club Role'
        verbose_name_plural = 'Club Roles'

class DistrictRole(models.Model):
    distRoleId = models.AutoField(primary_key=True)
    distRoleName = models.CharField(max_length=15,verbose_name = "District Role Name")

    def __str__(self):
        return f'{self.distRoleName}'

    class Meta:
        verbose_name = 'District Role'
        verbose_name_plural = 'District Roles'

class DistrictCouncil(models.Model):
    distId =  models.ForeignKey(District, on_delete = models.CASCADE)
    districtRole = models.ForeignKey(DistrictRole, on_delete = models.CASCADE)
    accountId = models.ForeignKey(Account, on_delete = models.CASCADE)
    tenureStarts = models.DateTimeField(verbose_name = "Tenure starts on")
    tenureEnds = models.DateTimeField(verbose_name = "Tenure ends on", blank = True)
    status = models.BooleanField('District Council Status', default=True)

    def __str__(self):
        return f'{self.tenureStarts+"-"+self.districtRole.distRoleName}'

    class Meta:
        verbose_name = 'District Council Member'
        verbose_name_plural = 'District Council Members'

    def save(self, *args, **kwargs):
        try:
            startDate = self.tenureStarts
            endDate = startDate + timedelta(days=365)
            self.tenureEnds = endDate
        except Exception as e:
            print(e)

        super().save(*args, **kwargs)

class ClubCouncil(models.Model):
    clubId =  models.ForeignKey(Club, on_delete = models.CASCADE)
    clubRole = models.ForeignKey(ClubRole, on_delete = models.CASCADE)
    accountId = models.ForeignKey(Account, on_delete = models.CASCADE)
    tenureStarts = models.DateTimeField(verbose_name = "Tenure starts on")
    tenureEnds = models.DateTimeField(verbose_name = "Tenure ends on", blank = True)
    status = models.BooleanField('Club Council Status', default=True)

    def __str__(self):
        return f'{self.clubId.clubName+"-"+self.clubRole.clubRoleName}'

    class Meta:
        verbose_name = 'BOD Member'
        verbose_name_plural = 'BOD Members'

    def save(self, *args, **kwargs):
        try:
            startDate = self.tenureStarts
            endDate = startDate + timedelta(days=365)
            self.tenureEnds = endDate
        except Exception as e:
            print(e)

        super().save(*args, **kwargs)