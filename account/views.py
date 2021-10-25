from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
import requests

def login(request):
    if request.method =='GET':
        return render(request,'login.html')
    elif request.method =="POST":
        userid = request.POST.get("username")
        pwd    = request.POST.get("password")
        user = None
        testuser = ["telkorea", "telkorea"]
        if testuser[0] == userid:
            if testuser[1] == pwd:
                user = True
        if user is not None:
            return redirect('/login_next')#로그인됐을 때
        else:
            return render(request,"login.html",{"message":"아이디/비밀번호를 다시 확인해주세요"})
            #로그인 안됐을때
