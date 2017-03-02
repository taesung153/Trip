from __future__ import unicode_literals
from ..login.models import User
import time, re
from django.db import models

class TripsManager(models.Manager):
    def validate(self, postData):
        errors = []
        today = time.strftime("%Y-%m-%d")
        DATE_REGEX = re.compile(r'^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$')
        if len(postData['destination']) < 1:
            errors.append("Destination cannot be blank.")
        if len(postData['description']) < 1:
            errors.append("Description cannot be blank.")
        if len(postData['travel_start']) < 1:
            errors.append("Travel start date cannot be blank.")
        if len(postData['travel_end']) < 1:
            errors.append("Travel end date cannot be blank.")
        if postData['travel_start'] < today:
            errors.append("Must be a future date. Cannot add dates before today.")
        if postData['travel_end'] < postData['travel_start']:
            errors.append("Travel end date must be later than travel start date")
        if not DATE_REGEX.match(postData['travel_start']):
            errors.append("Dates must be in YYYY-MM-DD format")
        if not DATE_REGEX.match(postData['travel_end']):
            errors.append("Dates must be in YYYY-MM-DD format")
        return errors

    def add(self, postData, user):
        trip = Trips.objects.create(destination = postData['destination'],
                                     description = postData['description'],
                                     travel_start = postData['travel_start'],
                                     travel_end = postData['travel_end'],
                                     user = user)
        return trip

    def makeChanges(self, postData, id):
        Items.objects.filter(id=id).update(content = postData['content'])

class Trips(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    travel_start = models.DateField()
    travel_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    objects = TripsManager()

class UserTripsManager(models.Manager):
    def add(self, user, trip):
        UserTrips.objects.create(user = user,
                                 trip = trip)

class UserTrips(models.Model):
    user = models.ForeignKey(User)
    trip = models.ForeignKey(Trips)
    objects = UserTripsManager()
