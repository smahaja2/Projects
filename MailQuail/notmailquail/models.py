# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from oauth2client.django_orm import CredentialsField

class Account(models.Model):
    address = models.CharField(primary_key=True, max_length=255)
    key = models.CharField(max_length=255, blank=True)
    username = models.ForeignKey('Users', db_column='username', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'account'

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class GoogleCredentialsCredentials(models.Model):
    id = models.IntegerField(primary_key=True)
    client_id = models.CharField(max_length=128)
    credentials = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'google_credentials_credentials'

class Mail(models.Model):
    address = models.ForeignKey(Account, db_column='address')
    time = models.IntegerField()
    name = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    labels = models.CharField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    body = models.CharField(max_length=255, blank=True)
    sender = models.CharField(max_length=255, blank=True)
    tid = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'mail'

class Reminder(models.Model):
    emailhash = models.CharField(primary_key=True, max_length=255)
    time = models.IntegerField(blank=True, null=True)
    pushn = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'reminder'

class SocialAuthAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)
    class Meta:
        managed = False
        db_table = 'social_auth_association'

class SocialAuthCode(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=75)
    code = models.CharField(max_length=32)
    verified = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'social_auth_code'

class SocialAuthNonce(models.Model):
    id = models.IntegerField(primary_key=True)
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)
    class Meta:
        managed = False
        db_table = 'social_auth_nonce'

class SocialAuthUsersocialauth(models.Model):
    id = models.IntegerField(primary_key=True)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser)
    class Meta:
        managed = False
        db_table = 'social_auth_usersocialauth'

class Users(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    number = models.IntegerField(blank=True, null=True)
    last = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'users'
        
class CredentialsModel(models.Model):
    address = models.CharField(primary_key=True, max_length=255)
    credential = CredentialsField()
    class Meta:
        db_table = 'cred'

