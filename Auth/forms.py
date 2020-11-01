from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import Account, Club, Member
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.translation import gettext as _

class AccountCreationForm(UserCreationForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email','autocomplete':'off'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username','autocomplete':'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }
    ))

    firstName = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name','autocomplete':'off'}))
    lastName = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name','autocomplete':'off'}))
    
    class Meta:
        model = Account
        fields = ('username', 'firstName','lastName','email', 'password1', 'password2',)       

class AccountChangeForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ['username']       

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Incorrect username or password'
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'id':'','class': 'ifb','autocomplete':'off','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'ifb',
            'id' : 'password',
            'placeholder':'Password'
        }
))

class PasswordChange(PasswordChangeForm):
    error_css_class = 'error'
    old_password = forms.CharField(required=True, 
                    widget=forms.PasswordInput(attrs={
                    'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(required=True,
                    widget=forms.PasswordInput(attrs={
                    'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(required=True,
                    widget=forms.PasswordInput(attrs={
                    'class': 'form-control', 'placeholder': 'Confirm Password'}))


class UserProfileUpdateForm(forms.ModelForm) :
    
    bloodGroups = (
("NA","Unknown" ),
("A+","A  positive" ),
("A-","A  negative" ),
("B+","B  positive" ),
("B-","B  negative" ),
("O+","O  positive" ),
("O-","O  negative" ),
("AB+","AB  positive "),
("AB-","AB  negative "),
)

    class Meta :
        model = Member
        fields = ['firstName','lastName','contact','bloodGroup','birthDate','photo','joiningDate']       
        labels = {
        "birthDate": "Birth Date",
        "joiningDate": "Joining Date"
        }

    photo = forms.ImageField(required=False, widget=forms.FileInput())
    # zone = forms.CharField(required=False, widget=forms.TextInput(attrs={
    #     'type': 'text',
    #     'value':0
    # }))
    birthDate = forms.DateField(label='Birth Date',required=False, widget=forms.DateInput(attrs={
                    'type': 'date'}))
    joiningDate = forms.DateField(label='Joining Date',required=False, widget=forms.DateInput(attrs={
                    'type': 'date'}))
    bloodGroup = forms.ChoiceField(choices = bloodGroups)
    
class EmailUpdateForm(forms.ModelForm) :
        
    class Meta :
        model = Club
        fields = ['clubName']       