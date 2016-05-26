from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import httplib2
from notmailquail.models import CredentialsModel
from time import mktime, strptime
from datetime import datetime
from django.db import connection, transaction

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets

from oauth2client.django_orm import Storage

from oauth2client.tools import run

import base64

import email

import datetime
import re
import requests
import json


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret_321385021897-tv7ictu5at1mlumrmstig58nfukbn7qn.apps.googleusercontent.com.json'

#Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
#OAUTH_SCOPE = 'https://www.googleapis.com/auth/plus.me'


flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE, redirect_uri='http://mailquail2.herokuapp.com/test/')

def index(request):
    if 'id' in request.session:
        return main(request, 'All')
    else:
        return render(request, 'login.html' )



def logback_request(request):
    return HttpResponseRedirect("/")

def logout_request(request):
    request.session.flush() 
    return render(request, 'logout.html')

def login_request(request):
    if 'id' in request.session:
        return HttpResponseRedirect("/")
    if 'username' in request.POST and request.POST['username'] and 'password' in request.POST and request.POST['password']:
        if 'choice' in request.POST and request.POST['choice']:
            if(request.POST['choice'] == "login"):
                row = checkUser(request.POST['username'], request.POST['password'])
                if row:
                    request.session['id'] = request.POST['username']
                    return HttpResponseRedirect("/")
                    #return render(request, 'Display.html', {'name' : str(request.POST['username']), 'user_list' : row, 'login' : True})
                else:
                    return render(request, 'login.html', {'error': True})
                    
            elif(request.POST['choice'] == "register"):
                return registerUser(request, request.POST['username'], request.POST['password'])
                
            elif(request.POST['choice'] == "delete"):
                row = checkUser(request.POST['username'], request.POST['password'])
                if row:
                    deleteUser(request.POST['username'], request.POST['password'])
                    return render(request, 'Display.html', {'delete' : True})
                else:
                    return render(request, 'login.html', {'error': True})
                
            else:
                row = checkUser(request.POST['username'], request.POST['password'])
                if row:
                    return render(request, 'Display.html', {'name' : str(request.POST['username']), 'change' : True})
                else:
                    return render(request, 'login.html', {'error': True})
    else:
        return render(request, 'login.html', {'error': True})

def change(request):
    if 'username' in request.POST and request.POST['username'] and 'oldpassword' in request.POST and request.POST['oldpassword']:
        if('newpassword' in request.POST and request.POST['newpassword']):
            row = checkUser(request.POST['username'], request.POST['oldpassword'])
            if row:
                changeUser(request.POST['username'], request.POST['oldpassword'], request.POST['newpassword'])
                row = checkUser(request.POST['username'], request.POST['newpassword'])
                return render(request, 'Display.html', {'name' : str(request.POST['username']), 'user_list' : row, 'login' : True})
            else:
                return render(request, 'Display.html', {'name' : str(request.POST['username']), 'error': True, 'change' : True})
                
        else:
             return render(request, 'Display.html', {'name' : str(request.POST['username']), 'error': True, 'change' : True})
             
    else:
         return render(request, 'Display.html', {'name' : str(request.POST['username']), 'error': True, 'change' : True})


def main(request, which):
    #emails = {"hi": "hi", "sup" : "sup", "how" : "how is it going", "yo" : "yo"}
    u = getArchivedEmails(request.session['id'], which)
    accounts2 = getAccounts(request.session['id'])
    accounts = []
    for a in accounts2:
        accounts.append(a[0])
    ret = []
#    t = getmail(request, accounts2[1][0])
#    return HttpResponse(t)
#    return render(request, 'temp.html', {'name' : request.session["id"], 'emails' : t, 'accounts' : accounts})

    if which == 'All':
        for account in accounts2:
            t = getmail(request, account[0])
            if type(t) is list:
                for mail in t:
                    ret.append(mail)
            else:
                return test_auth(request)
    else:
        t = getmail(request, which)
        if type(t) is list:
            for mail in t:
                ret.append(mail)
        else:
            test_auth(request)
    for mail in ret:
        m = re.match(".{25}", mail[1])
        if m:
            v = m.group(0)
            v = str.strip(v)
            tim = strptime(v, "%a, %d %b %Y %H:%M:%S")
            stamp = mktime(tim)
            mail.append(stamp)
        else:
            mail.append(0)
    sorted(ret, key=lambda ret: ret[7])

        
        
    return render(request, 'temp.html', {'name' : request.session["id"], 'emails' : ret, 'accounts' : accounts})
    
def archive(request):
    address = request.POST['Address']
    time = request.POST['Time']
    sendername = request.POST['Sender']
    subject = request.POST['Subject']
    mid = request.POST['Id']
    body = request.POST['Body'][:2000]
    sendermail = request.POST['Sender_Mail']
    from django.db import connection, transaction
    cursor = connection.cursor()
     # Data retrieval operation - no commit required
    cursor.execute("SELECT * FROM Mail WHERE id = %s", [mid])
    rows = cursor.fetchall()
    if rows:
        return HttpResponseRedirect("/")
    else:
        cursor.execute("INSERT INTO Mail (address, time, sendername, subject, id, body, sendermail) VALUES (%s, %s, %s, %s, %s, %s, %s)", [address, time, sendername, subject, mid, body, sendermail])
        transaction.commit_unless_managed()
        return HttpResponseRedirect("/")
        
    
def getAccounts(username):
    from django.db import connection, transaction
    cursor = connection.cursor()
     # Data retrieval operation - no commit required
    cursor.execute("SELECT * FROM Account WHERE username = %s", [username])
    rows = cursor.fetchall()
    return rows


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
    
def registerUser(request, username, password):
    row = checkUser(username, password)
    if(row):
        return render(request, 'login.html', {'error': True})
    from django.db import connection, transaction
    cursor = connection.cursor()
    #if(cursor.execute("SELECT name FROM Users WHERE username = %s", [username]).fetchone().
    cursor.execute("INSERT INTO Users (username, password, name, number, last) VALUES (%s, %s, %s, '0', '0')", [username, password, username])
    transaction.commit_unless_managed()
    return render(request, 'login.html', {'registered': True})

def deleteUser(username, password):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Users WHERE username=%s AND password=%s", [username, password])
    transaction.commit_unless_managed()

def changeUser(username, oldpassword, newpassword):
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("UPDATE Users SET password=%s WHERE username=%s AND password=%s", [newpassword, username, oldpassword])
    transaction.commit_unless_managed()
    

def test_auth(request):
    auth_uri = flow.step1_get_authorize_url()
    return HttpResponseRedirect(auth_uri)
    
def save(request):
    credential = flow.step2_exchange(request.REQUEST)
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("gmail", "v1", http=http)
    addressResponse = service.users().getProfile(userId='me').execute(http=http)
    emailAddress = addressResponse['emailAddress']
    storage = Storage(CredentialsModel, 'address', emailAddress, 'credential')
    storage.put(credential)
    from django.db import connection, transaction
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Account WHERE address = %s", [emailAddress])
    row = cursor.fetchone()
    if row:
        return HttpResponseRedirect("/")
    cursor.execute("INSERT INTO Account (address, key, username) VALUES (%s, %s, %s)", [emailAddress, 1234, request.session['id']])
    transaction.commit_unless_managed()
    return HttpResponseRedirect("/")
    
   
def getmail(request, address):
    storage = Storage(CredentialsModel, 'address', address, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        auth_uri = flow.step1_get_authorize_url()
        return HttpResponseRedirect(auth_uri)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("gmail", "v1", http=http)
        response = service.users().messages().list(userId='me',q='', maxResults=6).execute(http=http)
        
        addressResponse = service.users().getProfile(userId='me').execute(http=http)
        emailAddress = addressResponse['emailAddress']
        #return HttpResponse(credential.to_json())
        
        bodies = []
        currIndex = 0
        for message in response['messages']:
            realMessage = service.users().messages().get(id=message['id'], userId='me', format='raw').execute(http=http)
            part = {}
            mid = message['id']
            message = base64.urlsafe_b64decode(realMessage['raw'].encode("utf-8"))
            #bodies.append(message)
            
            bodyBody = ""
            
            b = email.message_from_string(message)
            if b.is_multipart():
                for payload in b.get_payload():
                    # if payload.is_multipart(): ...
                    bodyBody = payload.get_payload()
            else:
                bodyBody = b.get_payload()
                
            address = b['from']
            
            p = re.compile("domain\ of\ ([^\ ]+\ ){1}")
            fromMail = re.search(p, message)
            #p = re.compile("quoted-printable([^\ ]+\ )+")
            #bodyBody = re.search(p, message)
            #p = re.compile("From: \"([^\"]+)\"")
            #fromStr = re.search(p, message)
            p = re.compile("Subject: (.+) From") 
            title = re.search(p, message)
            #p = re.compile("Received: by .+; (.+) -.+ X-Received:")
            p = re.compile("...,\ [0-9]\ ...\ [0-9]{4}\ ..\:..\:..")
            time = re.search(p, message)
            tr = r'Received: by .+; (.+) -.+ X-Received:'
            #time = re.findall(tr, message)
            
            p = re.compile("[^<]+")
            addressPart1 = re.search(p, address)
            p = re.compile("<[^>]+>")
            addressPart2 = re.search(p, address)
            
            addressSplit = address.split("<")
            part['address'] = emailAddress
            part['time'] = b['date']#time.group(0) if time != None else time
            part['name'] = addressPart1.group(0)#fromStr.group(0) if fromStr != None else fromStr
            part['title'] = b['subject']#title.group(0) if title != None else title
            part['id'] = mid
            part['body'] = realMessage['snippet']#.group(0) if bodyBody != None else bodyBody
            part['sender'] = addressPart2.group(0)#fromMail.group(0) if fromMail != None else fromMail
            #if(fromMail != None):
                #formatted = fromMail.group(0).replace("domain of ", "")
                #part['sender'] = formatted
            #if(fromStr != None):
                #formatted = fromStr.group(0).replace("From: ", "")
                #part['name'] = formatted
            listForDatabase = [emailAddress, part['time'], part['name'], part['title'], mid, part['body'], part['sender']]
            bodies.append(listForDatabase)
        return bodies
        
    
def decode_base64(data):
    """Decode base64, padding being optional.

    :param data:
    Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
    return base64.decodestring(data)
    
def gmail_login_request(request):
    import httplib2

    from apiclient.discovery import build
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from oauth2client.tools import run
    
    
    # Path to the client_secret.json file downloaded from the Developer Console
    CLIENT_SECRET_FILE = 'client_secret_321385021897-tv7ictu5at1mlumrmstig58nfukbn7qn.apps.googleusercontent.com.json'
    
    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
    
    # Location of the credentials storage file
    STORAGE = Storage('gmail.storage')
    
    # Start the OAuth flow to retrieve credentials
#    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()
    
    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        credentials = run(flow, STORAGE, http=http)
    
    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)
    
    # Build the Gmail service from discovery
    gmail_service = build('gmail', 'v1', http=http)
    
    # Retrieve a page of threads
    threads = gmail_service.users().threads().list(userId='me').execute()
    
    # Print ID for each thread
    if threads['threads']:
        for thread in threads['threads']:
            print 'Thread ID: %s' % (thread['id'])
        
        
def search(request):
    if 'query' in request.POST and request.POST['query']:
        cursor = connection.cursor()
        cursor.execute("SELECT Mail.address, Mail.time, Mail.sendername, Mail.subject, Mail.id, Mail.body, Mail.sendermail FROM Mail INNER JOIN Account ON Mail.address = Account.address WHERE Account.username = %s AND (Mail.subject LIKE %s OR Mail.body LIKE %s)", [request.session['id'], "%" + request.POST['query'] + "%", "%" +request.POST['query'] + "%"])
        rows = cursor.fetchall()
        accounts = getAccounts(request.session['id'])
        acc = []
        for account in accounts:
            acc.append(account[0])
        #return HttpResponse(rows)
        return render(request, 'temp.html', {'name' : request.session["id"], 'emails' : rows, 'accounts' : acc})
        
def listMessages(userID):
    return ['Test Message ID']
        
def getSpecificMessage(messageID):
    return ['Test Message Body']