from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import re
import cv2
import numpy as np
import pandas as pd
import random
import joblib
import os
global model    

def Admin(request):
    if request.method == 'GET':
       return render(request, 'Admin.html', {})
       
def AdminLogin(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      if username == 'admin' and password == 'admin':
       context= {'data':'welcome '+username}
       return render(request, 'AdminScreen.html', context)
      else:
       context= {'data':'login failed'}
       return render(request, 'Admin.html', context)

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})
       
def Accuracy(request):
    if request.method == 'GET':
       return render(request, 'Accuracy.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})
       
def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def ChangePassword(request):
    if request.method == 'GET':
       return render(request, 'ChangePassword.html', {})

def Prediction(request):
    if request.method == 'GET':
       return render(request, 'Prediction.html', {})
def getPostData():
    output =''
    output+=""        
    return output

def ChangeMyPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
                        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update register set password='"+password+"' where username='"+user+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        status_data = ''
        if db_cursor.rowcount == 1:
            con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
            with con:
                cur = con.cursor()
                cur.execute("select * FROM register")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] == user and row[1] == password:
                        status_data = row[5]
                        break
            if status_data == 'none':
                status_data = ''   
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+user+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+user+'</font></td></tr></table></br></br>'
            output+=getPostData()
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Updated Password'}
            return render(request, 'UserScreen.html', context)
            
            
            
def UpdateStatus(request):
    if request.method == 'GET':
       return render(request, 'UpdateStatus.html', {})

def UpdateMyStatus(request):
    if request.method == 'POST':
        status = request.POST.get('status', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
                        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update register set status='"+status+"' where username='"+user+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        if db_cursor.rowcount == 1:
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+user+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status+'</font></td><td><font size=3 color=black>welcome : '+user+'</font></td></tr></table></br></br>'
            output+=getPostData()
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Error in updating status'}
            return render(request, 'UpdateStatus.html', context)  


def EditProfile(request):
    if request.method == 'GET':
        output = ''
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        output = ''
        username = ''
        password = ''
        contact = ''
        email = ''
        address = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register where username='"+user+"'")
            rows = cur.fetchall()
            for row in rows:
                username = row[0]
                password = row[1]
                contact = row[2]
                email = row[3]
                address = row[4]
        output+='<tr><td><b>Username</b></td><td><input type=text name=username style=font-family: Comic Sans MS size=30 value='+username+' readonly></td></tr>'
        output+='<tr><td><b>Password</b></td><td><input type=password name=password style=font-family: Comic Sans MS size=30 value='+password+'></td></tr>'
        output+='<tr><td><b>Contact&nbsp;No</b></td><td><input type=text name=contact style=font-family: Comic Sans MS size=20 value='+contact+'></td></tr>'
        output+='<tr><td><b>Email&nbsp;ID</b></td><td><input type=text name=email style=font-family: Comic Sans MS size=40 value='+email+'></td></tr>'
        output+='<tr><td><b>Address</b></td><td><input type=text name=address style=font-family: Comic Sans MS size=60 value='+address+'></td></tr>'
        context= {'data':output}
        return render(request, 'EditProfile.html', context)    

def Signup(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      myfile = request.FILES['image']
      fs = FileSystemStorage()
      filename = fs.save('C:/Users/madha/OneDrive/Desktop/Project/Analyze and forecast the cyber attack detection process using Machine Learing Techniques/User/static/profiles/'+username+'.png', myfile)
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(username,password,contact,email,address,status) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"','none')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)

def EditMyProfile(request):
    if request.method == 'POST':
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      myfile = request.FILES['image']

      if os.path.exists('C:/Users/madha/OneDrive/Desktop/Project/Analyze and forecast the cyber attack detection process using Machine Learing Techniques/User/static/profiles/'+username+'.png'):
          os.remove('C:/Users/madha/OneDrive/Desktop/Project/Analyze and forecast the cyber attack detection process using Machine Learing Techniques/User/static/profiles/'+username+'.png')

      fs = FileSystemStorage()      
      filename = fs.save('C:/Users/madha/OneDrive/Desktop/Project/Analyze and forecast the cyber attack detection process using Machine Learing Techniques/User/static/profiles/'+username+'.png', myfile)
      
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "update register set username='"+username+"',password='"+password+"',contact='"+contact+"',email='"+email+"',address='"+address+"' where username='"+username+"'"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record updated")
      status_data = ''
      if db_cursor.rowcount == 1:
          con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
          with con:
              cur = con.cursor()
              cur.execute("select * FROM register")
              rows = cur.fetchall()
              for row in rows:
                  if row[0] == username and row[1] == password:
                      status_data = row[5]
                      break
          if status_data == 'none':
              status_data = ''            
          output = ''
          output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+username+'.png width=200 height=200></img></td>'
          output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+username+'</font></td></tr></table></br></br>'
          output+=getPostData()
          context= {'data':output}
          return render(request, 'UserScreen.html', context)
      else:
       context= {'data':'Updated in editing profile'}
       return render(request, 'UserScreen.html', context)    
        
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        status_data = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    status = 'success'
                    status_data = row[5]
                    break
        if status_data == 'none':
            status_data = ''
        if status == 'success':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+username+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+username+'</font></td></tr></table></br></br>'
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)

def ViewUsers(request):
    if request.method == 'GET':
       strdata = '<table border=1 align=center width=50%><tr><th>User Name</th><th>Email</th><th>Address</th><th>Contact</th><th>Image</th></tr><tr>'
       con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
       with con:
          cur = con.cursor()
          cur.execute("select * FROM register")
          rows = cur.fetchall()
          for row in rows: 
             strdata+='<td>'+row[0]+'</td><td>'+row[3]+'</td><td>'+str(row[4])+'</td><td>'+str(row[2])+'</td><td><img src=/static/profiles/'+row[0]+'.png width=200 height=200></img></td></tr>'
    context= {'data':strdata}
    return render(request, 'Viewusers.html', context)
            
def ViewUser(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register where username='"+user+"' ")
            rows = cur.fetchall()
            for row in rows: 
               output=''
               output= '<table border=1 align=center width=50%><tr><th>User Name</th><th>Email</th><th>Address</th><th>Contact</th><th>Image</th></tr><tr>'
               output+='<td>'+row[0]+'</td><td>'+row[3]+'</td><td>'+str(row[4])+'</td><td>'+str(row[2])+'</td>'
               output+='<td><img src=/static/profiles/'+user+'.png width=200 height=200></img></td></tr></table></br></br>'
               context= {'data':output}
               return render(request, 'Viewuser.html', context)
               
               
               
               
def HomePage(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        status_data = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'Intrusion',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == user:
                    status_data = row[5]
                    break
            if status_data == 'none':
                status_data = ''   
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+user+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+user+'</font></td></tr></table></br></br>'
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
       
def Predict(request):
    context = {}  # Initialize context outside the if-else block

    if request.method == 'POST':
        model = joblib.load('model.pkl')

        # Ensure numeric inputs and handle empty fields
        int_features = [
            float(request.POST.get('attack', 0)),
            float(request.POST.get('count', 0)),
            float(request.POST.get('dst_host_diff_srv_rate', 0)),
            float(request.POST.get('dst_host_same_src_port_rate', 0)),
            float(request.POST.get('dst_host_same_srv_rate', 0)),
            float(request.POST.get('dst_host_srv_count', 0)),
            float(request.POST.get('flag', 0)),
            float(request.POST.get('last_flag', 0)),
            float(request.POST.get('logged_in', 0)),
            float(request.POST.get('same_srv_rate', 0)),
            float(request.POST.get('serror_rate', 0)),
            float(request.POST.get('service_http', 0)),
        ]

        # Your existing feature engineering code
        if int_features[0] == 0:
            f_features = [0, 0, 0] + int_features[1:]
        elif int_features[0] == 1:
            f_features = [1, 0, 0] + int_features[1:]
        elif int_features[0] == 2:
            f_features = [0, 1, 0] + int_features[1:]
        else:
            f_features = [0, 0, 1] + int_features[1:]

        if f_features[6] == 0:
            fn_features = f_features[:6] + [0, 0] + f_features[7:]
        elif f_features[6] == 1:
            fn_features = f_features[:6] + [1, 0] + f_features[7:]
        else:
            fn_features = f_features[:6] + [0, 1] + f_features[7:]

        final_features = [np.array(fn_features)]
        predict = model.predict(final_features)

        if predict == 0:
            output = 'Normal'
        elif predict == 1:
            output = 'DOS'
        elif predict == 2:
            output = 'PROBE'
        elif predict == 3:
            output = 'R2L'
        else:
            output = 'U2R'

        context = {'data': 'Predicted Result:'+output}

    return render(request, 'Predict.html', context)
