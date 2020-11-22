from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm
from .forms import AccountCreationForm, AccountChangeForm
from .models import Account, Club, District, Member, ClubRole, DistrictRole, ClubCouncil, DistrictCouncil

class AccountAdmin(UserAdmin):
    verbose_name_plural = "Accounts"
    add_form = UserCreationForm
    add_fieldsets = ((None, {'fields': ('username', 'email','loginType',
    'password1', 'password2'), 'classes': ('wide',)}),)
    form = AccountChangeForm
    model = Account
    list_display = ['username','email','password','loginType']
    exclude = ('first_name','last_name')
    fieldsets = (
        ('Personal info', {'fields': ('username','password','loginType','email')}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(Club)
admin.site.register(District)
admin.site.register(Member)
admin.site.register(ClubRole)
admin.site.register(DistrictRole)
admin.site.register(ClubCouncil)
admin.site.register(DistrictCouncil)
admin.site.unregister(Group)