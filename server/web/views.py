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
from users.models import get_user_hospital, get_user_profile
from django.core.exceptions import PermissionDenied
from biblio.forms import PaperForm, SpecialityForm, SourceForm
from web.forms import RegistrationForm
import os
from django.http import FileResponse
from stock.utils import dump_csv
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        profile = get_user_profile(request.user)
        if profile is not None:
            if profile.is_medical:
                return patient(request)
            elif profile.is_logistic:
                return stock(request)
            elif profile.is_politic:
                return export_csv(request)

    return render(request, "web/index.html", {})


def registration(request):
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            hospital_name = form.cleaned_data['hospital_name']
            contact_name = form.cleaned_data['contact_name']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            country = form.cleaned_data['country']
            dect = form.cleaned_data['dect']
            contact = form.cleaned_data['contact']
            message = f"{hospital_name}\n{contact_name}\n{address}\n{postcode}\n{country}\n{dect}\n{contact}"
            try:
                send_mail(f"Inscription {hospital_name}", message, "registrations@covid-data.fr", ['registrations@covid-data.fr'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('/registration/done')
    return render(request, "web/registration.html", {'form': form})


def registration_done(request):
    return HttpResponse("Votre inscription a été prise en compte, vous recevrez sous peu un mail de confirmation à l'adresse fournie")


@login_required
def patient(request):
    profile = get_user_profile(request.user)
    link = {'main': "", "2": ""}
    # js = {"version": os.getenv("JS_VERSION")}
    js = {"main": os.getenv("JS_MAIN_PATIENT"),
          "2": os.getenv("JS_2_PATIENT")}
    hospital = get_user_hospital(request.user)
    return render(request, "web/patient.html",
                  {"link": link,
                   "js": js,
                   "hospital": hospital,
                   "profile": profile})


@login_required
def stock(request):
    profile = get_user_profile(request.user)
    link = {'main': "", "2": ""}
    js = {"main": os.getenv("JS_MAIN_STOCK"),
          "2": os.getenv("JS_2_STOCK")}

    hospital = get_user_hospital(request.user)
    return render(request, "web/stock.html",
                  {"link": link,
                   "js": js,
                   "hospital": hospital,
                   "profile": profile})


def opendata(request):
    if request.user.is_authenticated:
        profile = get_user_profile(request.user)
    else:
        profile = None
    link = {'main': "", "2": ""}
    # js = {"version": os.getenv("JS_VERSION")}
    js = {"main": os.getenv("JS_MAIN_OPENDATA"),
          "2": os.getenv("JS_2_OPENDATA")}

    return render(request, "web/opendata.html",
                  {"link": link, "js": js, "profile": profile})


@login_required
def add_paper(request, obj: str = None):

    if obj == "paper":
        print(request.FILES)
        paper_form = PaperForm(request.POST, request.FILES)
        if paper_form.is_valid():
            paper_form.save()
    else:
        paper_form = PaperForm()

    if obj == "spec":
        spec_form = SpecialityForm(request.POST)
        if spec_form.is_valid():
            spec_form.save()
    else:
        spec_form = SpecialityForm()

    if obj == "src":
        src_form = SourceForm(request.POST)
        if src_form.is_valid():
            src_form.save()
    else:
        src_form = SourceForm()

    forms = [
        {'form': spec_form, "title": "Ajout d'une nouvelle spécialité",
         "obj": "spec"},
        {'form': paper_form, "title": "Ajout d'un nouvel article",
         "obj": "paper"},
        {'form': src_form, "title": "Ajout d'une nouvelle source",
         "obj": "src"}
    ]
    return render(request, "web/paper.html", {"forms": forms})


@login_required
def export_csv(request):
    profile = get_user_profile(request.user)
    link = {'main': "", "2": ""}
    # js = {"version": os.getenv("JS_VERSION")}
    js = {"main": os.getenv("JS_MAIN_HOSPITAL"),
          "2": os.getenv("JS_2_HOSPITAL")}

    hospital = get_user_hospital(request.user)
    return render(request, "web/hospitals_visu.html",
                  {"link": link,
                   "js": js,
                   "hospital": hospital,
                   "profile": profile})
