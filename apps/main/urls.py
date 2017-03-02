from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'add$', views.add, name = 'add'),
    url(r'addTravelPlan$', views.addTravelPlan, name = 'addTravelPlan'),
    url(r'addToMyTrips/(?P<id>\d+)$', views.addToMyTrips, name = "addToMyTrips"),
    url(r'destination/(?P<id>\d+)$', views.destination, name = 'destination'),
    url(r'makeChanges/(?P<id>\d+)$', views.makeChanges, name = 'makeChanges'),
    url(r'delete/(?P<id>\d+)$', views.delete, name = 'delete'),
    url(r'logout$', views.logout, name = 'logout'),
]
