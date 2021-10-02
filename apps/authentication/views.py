# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from accounts.models import Profile


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            
            try:
                    
                # print(username)
                obj1 = User.objects.get(username = username)
                # print(obj1)
            
                if(obj1 != None):
                    obj2 = Profile.objects.get(user = obj1)
                    user_type = obj2.User_Type
                    if(user_type == 'Artist'):
                        # First authenticate the user (CHECK USERNAME AND PASSWORD)
                        user = authenticate(username=username, password=password)
                        
                        if user is not None:
                            # if user is authenticated then and then it will enter inside IF block and then LOGIN allowed
                            if(obj2.admin_approval_status):
                                login(request, user)
                                request.session['name'] = obj1.first_name
                                request.session['username'] = obj1.username
                                request.session['id'] = obj1.id
                                return redirect("/artist/index/")
                            else:
                                msg = "Please wait till Admin approves the your registration request"
                        else:
                            msg = 'Invalid credentials'
                    else:
                        msg = "Sorry..!! only 'Artist' users are allowed to be Logged-In here."
                else:
                    msg = "Sorry..!! you are not registered with our System, Contact Admin"
            except:
                msg = "Sorry..!! you are not registered with our System, Contact Admin"
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


# def register_user(request):
#     msg = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             raw_password = form.cleaned_data.get("password1")
#             user = authenticate(username=username, password=raw_password)

#             msg = 'User created - please <a href="/login">login</a>.'
#             success = True

#             # return redirect("/login/")

#         else:
#             msg = 'Form is not valid'
#     else:
#         form = SignUpForm()

#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
