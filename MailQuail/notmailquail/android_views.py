from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
import requests
import json
import re

@csrf_exempt
def a_login(request):
    if 'username' in request.POST and request.POST['username'] and 'password' in request.POST and request.POST['password']:
        if('choice' in request.POST and request.POST['choice']):
            if(request.POST['choice'] == "login"):
                row = checkUser(request.POST['username'], request.POST['password'])
                if row:
                    resp = {}
                    resp['status'] = 'Success'
                    return HttpResponse(json.dumps(resp), content_type="application/json")
             
                else:
                    resp = {}
                    resp['status'] = 'Failure'
                    return HttpResponse(json.dumps(resp), content_type="application/json") 
                   
                    
            elif(request.POST['choice'] == "register"):
                return registerUser(request.POST['username'], request.POST['password'])
    return HttpResponse(request.POST)

@csrf_exempt
def a_accounts(request):
    if 'username' in request.POST and request.POST['username']:
        accounts = getAccounts(request.POST['username'])
        return HttpResponse(json.dumps(accounts), content_type="application/json")
    else:
        return HttpResponse("Hello")

@csrf_exempt        
def a_mail(request):
    if 'username' in request.POST and request.POST['username']:
        if 'account' in request.POST and request.POST['account']:
            emails = getArchivedEmails(request.POST['username'], request.POST['account'])
            return HttpResponse(json.dumps(emails), content_type="application/json")


def getAccounts(username):
    from django.db import connection, transaction
    cursor = connection.cursor()
     # Data retrieval operation - no commit required
    cursor.execute("SELECT * FROM Account WHERE username = %s", [username])
    rows = cursor.fetchall()
    return rows


#Database Queries
def getArchivedEmails(username, account):
    from django.db import connection, transaction
    cursor = connection.cursor()
    # Data retrieval operation - no commit required
    if account == "All":
        cursor.execute("SELECT * FROM Account WHERE username = %s", [username])
    else:
        cursor.execute("SELECT * FROM Account WHERE username = %s AND address = %s", [username, account])
    rows = cursor.fetchall()
    emails  = []
    for row in rows:
        cursor.execute("SELECT * FROM Mail WHERE address = %s", [row[0]])
        mail = cursor.fetchall()
        emails += mail
    return emails
    
def checkUser(username, password):
    from django.db import connection, transaction
    cursor = connection.cursor()
    # Data retrieval operation - no commit required
    cursor.execute("SELECT * FROM Users WHERE password = %s AND username = %s", [password, username])
    row = cursor.fetchone()
    return row
    
def registerUser(username, password):
    from django.db import connection, transaction
    cursor = connection.cursor()
    #if(cursor.execute("SELECT name FROM Users WHERE username = %s", [username]).fetchone().
    cursor.execute("INSERT INTO Users (username, password, name, number, last) VALUES (%s, %s, %s, '0', '0')", [username, password, username])
    transaction.commit_unless_managed()
    resp = {}
    resp['status'] = 'Success'
    return HttpResponse(json.dumps(resp), content_type="application/json")
  