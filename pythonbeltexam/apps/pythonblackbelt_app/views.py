# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . models import User, Trip
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def index(request):
    return render(request, 'pythonblackbelt_app/index.html')
def reg(request):
    user_data={
    "name" : request.POST['name'],
    "username" : request.POST['username'],
    "email" : request.POST['email'],
    "password" : request.POST['password'],
    "confirm_password" : request.POST['confirm_password']
    }
    result = User.objects.register(user_data)
    if result['errors'] == None:
        request.session['user_username'] = result['user'].username
        request.session['user_name'] = result['user'].name
        request.session['user_email'] = result['user'].email
        request.session['user_id'] = result['user'].id
        return redirect("/travels")
    else:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/main")
def login(request):
    user_data={
    "email" : request.POST['email'],
    "password" : request.POST['password']
    }
    result = User.objects.logger(user_data)
    if result['errors'] == None:
        request.session['user_username'] = result['user'].username
        request.session['user_name'] = result['user'].name
        request.session['user_email'] = result['user'].email
        request.session['user_id'] = result['user'].id
        return redirect("/travels")
    else:
        for error in result['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/main")
def travels(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/main')
    all_trips = Trip.objects.all()
    context={
    'all_trips' : all_trips,
    }
    return render(request, 'pythonblackbelt_app/trip.html', context)
def add(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/main')
    return render(request, 'pythonblackbelt_app/add.html')
def addplan(request):
    trip_data={
    "destination" : request.POST['destination'],
    "plan" : request.POST['plan'],
    "travel_start" : request.POST['travel_start'],
    "travel_end" : request.POST['travel_end'],
    }
    trip_result = Trip.objects.regtrip(trip_data)
    if trip_result['errors'] == None:
        request.session['trip_id']=trip_result['trip'].id
        id_data={
        "userid" : request.session['user_id'],
        "tripid" : request.session['trip_id']
        }
        useradd_result = Trip.objects.reguser(id_data)
        if useradd_result['errors'] == None:
            mytrip = Trip.objects.filter(user = User.objects.get(id = request.session['user_id']))
            context = {
                "mytrip" : mytrip
            }
            return redirect("/travels", context)
    else:
        for error in trip_result['errors']:
            messages.add_message(request, messages.ERROR, error)
        for error in user_result['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/add")
def destination(request,id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/main')
        trips = Trip.objects.filter(id=id)
        context={
            "trips" : trip
        }
    return render(request, 'pythonblackbelt_app/destination.html', context)
def logout(request):
	request.session.clear()
	return redirect('/main')
