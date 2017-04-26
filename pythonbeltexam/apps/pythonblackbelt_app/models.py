# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django import forms
import re, bcrypt, string, datetime

class UserManager(models.Manager):

    def register(self, data):
        numCheck = False
        charCheck = False
        characters = list(string.letters)
        numbers = [str(i) for i in range(10)]
        EMAIL_REGEX = r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        errors = [] #store errors that occur during verification
        if len(data['name']) == 0:
            errors.append("Name may not be blank.")
        elif len(data['name']) < 3:
            errors.append("Name must at least have 2 characters.")
        if not data['name'].isalpha():
            errors.append("Name may only be letters.")
        if len(data['username']) == 0:
            errors.append("Username may not be blank.")
        elif len(data['username']) < 3:
            errors.append("Alias must at least have 2 characters.")
        if not data['username'].isalpha():
            errors.append("Username may only be letters.")
        if len(data['email']) < 8:
            errors.append("Email must at least have 8 characters.")
        if not re.match(EMAIL_REGEX, data["email"]):
            errors.append("Email not in valid format.")
        for char in data['password']:
            if not charCheck:
                if char in characters:
                    charCheck = True
            if not numCheck:
                if char in numbers:
                    numCheck = True
            if numCheck and charCheck:
                break
        if not numCheck or not charCheck:
            errors.append("Your password must include at least one letter and at least one number.")
        if len(data['password']) < 8:
            errors.append("Password must at least have 8 characters.")
        if data['password'] != data['confirm_password']:
            errors.append("Password is not matching confirm password!")

        try:
            User.objects.get(email=data['email'])
            errors.append("You already have an account!")
        except:
            pass
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        if len(errors) == 0:#log in if there are no errors and create profile
            user = User.objects.create(name=data['name'], username=data['username'], email=data['email'], password=data['password'])
            return{"user" : user, "errors" : None}
        else:
            return{"user" : None, "errors" : errors}
    def logger(self, data):
        errors = []
        try:
            found_user = User.objects.get(email=data['email'])
            if bcrypt.hashpw(data['password'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
				errors.append("Incorrect password.")
        except:
			errors.append("Email address not registered.")
        if len(errors) == 0:
            user = User.objects.get(email=data['email'])
            return{"user" : user, "errors" : None}
        else:
            return{"user" : None, "errors" : errors}
class TripManager(models.Manager):
    def regtrip(self, data):
        errors = []
        if len(data['destination']) == 0:
            errors.append("Destination may not be blank.")
        if len(data['plan']) == 0:
            errors.append("Description may not be blank.")
        if len(data['travel_start']) == 0:
            errors.append("Travel Dates may not be blank.")
        elif datetime.datetime.strptime(data['travel_start'], '%Y-%m-%d') <= datetime.datetime.now():
			errors.append("Travel Start Dates may not be in the past!")
        if len(data['travel_end']) == 0:
            errors.append("Travel Dates may not be blank.")
        elif datetime.datetime.strptime(data['travel_end'], '%Y-%m-%d') <= datetime.datetime.strptime(data['travel_start'], '%Y-%m-%d'):
			errors.append("Travel End Dates may not be before you leave!")
        if len(errors) == 0:#log in if there are no errors and create profile
            trip = Trip.objects.create(destination=data['destination'], plan=data['plan'],travel_start=data['travel_start'], travel_end=data['travel_end'])
            return{"trip" : trip, "errors" : None}
        else:
            return{"trip" : None, "errors" : errors}
    def reguser(self, data):
        errors = []
        if errors:
            return{"trip" : None, "errors" : errors}
        else:
            currentuser = User.objects.get(id=data['userid'])
            thistrip = Trip.objects.get(id=data['tripid'])
            trip = thistrip.user.add(currentuser)
            return{"trip" : trip, "errors" : None}


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    travel_start = models.DateField()
    travel_end = models.DateField()
    plan = models.CharField(max_length=255)
    user = models.ManyToManyField(User, related_name="trip")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = TripManager()
