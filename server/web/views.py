"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View

from server import settings
from users.models import get_user_hospital, get_user_profile
from web.forms import RegistrationForm
import os
from django.http import HttpResponse


def index(request):
    return redirect("/beds")


@login_required
def patient(request):
    profile = get_user_profile(request.user)
    link = {'main': "", "2": ""}
    # js = {"version": os.getenv("JS_VERSION")}
    js = {"main": os.getenv("JS_MAIN_PATIENT"),
          "2": os.getenv("JS_2_PATIENT")}
    # hospital = get_user_hospital(request.user)
    return render(request, "web/patient.html",
                  {"link": link,
                   "js": js,
                   # "hospital": hospital,
                   "profile": profile})


@login_required
def beds(request):
    profile = get_user_profile(request.user)
    link = {'main': "", "2": ""}
    # js = {"version": os.getenv("JS_VERSION")}
    js = {"main": os.getenv("JS_MAIN_PATIENT"),
          "2": os.getenv("JS_2_PATIENT")}
    # hospital = get_user_hospital(request.user)
    return render(request, 'web/beds.html',
                  {"link": link,
                   "js": js,
                   # "hospital": hospital,
                   "profile": profile})
