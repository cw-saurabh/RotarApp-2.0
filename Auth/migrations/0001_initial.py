# Generated by Django 2.2.13 on 2020-09-06 00:19

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('clubId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('clubName', models.CharField(blank=True, default='', max_length=50, verbose_name='Name')),
                ('zone', models.CharField(blank=True, max_length=2, null=True, verbose_name='Zone')),
                ('clubLogo', models.ImageField(upload_to='clubLogos', verbose_name='Club Logo')),
                ('charterDate', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Charter Date')),
                ('meetingPlace', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Meeting Place')),
                ('rotaryId', models.CharField(blank=True, default='23', max_length=7, null=True, verbose_name='Rotary Id')),
            ],
            options={
                'verbose_name': 'Club',
                'verbose_name_plural': 'Clubs',
            },
        ),
        migrations.CreateModel(
            name='ClubRole',
            fields=[
                ('clubRoleId', models.AutoField(primary_key=True, serialize=False)),
                ('clubRoleName', models.CharField(max_length=15, verbose_name='Club Role Name')),
            ],
            options={
                'verbose_name': 'Club Role',
                'verbose_name_plural': 'Club Roles',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('distId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('distName', models.CharField(blank=True, max_length=5, null=True, verbose_name='District Id')),
                ('distLogo', models.ImageField(upload_to='distLogos', verbose_name='District Logo')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='DistrictRole',
            fields=[
                ('distRoleId', models.AutoField(primary_key=True, serialize=False)),
                ('distRoleName', models.CharField(max_length=15, verbose_name='District Role Name')),
            ],
            options={
                'verbose_name': 'District Role',
                'verbose_name_plural': 'District Roles',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('loginId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('loginType', models.CharField(choices=[('0', 'Rotaractor'), ('1', 'Admin')], default='0', max_length=2)),
                ('email', models.EmailField(max_length=254)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Username',
                'verbose_name_plural': 'Usernames',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('memberId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('firstName', models.CharField(blank=True, default='', max_length=15, verbose_name='First Name')),
                ('lastName', models.CharField(blank=True, default='', max_length=15, null=True, verbose_name='Last Name')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], default=None, max_length=1, null=True)),
                ('rotaryId', models.IntegerField(blank=True, null=True, verbose_name='Rotary Id')),
                ('contact', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Contact Number')),
                ('birthDate', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Birth Date')),
                ('bloodGroup', models.CharField(blank=True, default=None, max_length=3, null=True, verbose_name='Blood Group')),
                ('photo', models.ImageField(null=True, upload_to='profilePics', verbose_name='Photo')),
                ('joiningDate', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Joining Date')),
                ('login', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rotaractor',
                'verbose_name_plural': 'Rotaractors',
            },
        ),
        migrations.CreateModel(
            name='DistrictCouncil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenureStarts', models.DateTimeField(verbose_name='Tenure starts on')),
                ('tenureEnds', models.DateTimeField(blank=True, verbose_name='Tenure ends on')),
                ('status', models.BooleanField(default=True, verbose_name='District Council Status')),
                ('accountId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('distId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.District')),
                ('districtRole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.DistrictRole')),
            ],
            options={
                'verbose_name': 'District Council Member',
                'verbose_name_plural': 'District Council Members',
            },
        ),
        migrations.CreateModel(
            name='ClubCouncil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenureStarts', models.DateTimeField(verbose_name='Tenure starts on')),
                ('tenureEnds', models.DateTimeField(blank=True, verbose_name='Tenure ends on')),
                ('status', models.BooleanField(default=True, verbose_name='Club Council Status')),
                ('accountId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('clubId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.Club')),
                ('clubRole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.ClubRole')),
            ],
            options={
                'verbose_name': 'BOD Member',
                'verbose_name_plural': 'BOD Members',
            },
        ),
        migrations.AddField(
            model_name='club',
            name='distId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Auth.District'),
        ),
        migrations.AddField(
            model_name='club',
            name='login',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]