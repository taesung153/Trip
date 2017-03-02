from django.shortcuts import render, redirect
from .models import User, Trips, UserTrips
from django.contrib import messages

# Create your views here.
def index(request):
    if "id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    usersTrips = UserTrips.objects.filter(user=user).values_list('trip__id', flat=True)
    usersTripsList = list(usersTrips)
    context = { 'trips' : Trips.objects.filter().exclude(user=user),
                'userTrips' : UserTrips.objects.filter(user=user),
                'otherUserTrips' : Trips.objects.filter().exclude(id__in=usersTrips)}
    return render(request, 'main/index.html', context)

def addTravelPlan(request):
    if "id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')
    return render(request, 'main/add.html')

def add(request):
    errors = Trips.objects.validate(request.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/main/addTravelPlan')
    user = User.objects.get(id=request.session['id'])
    trip = Trips.objects.add(request.POST, user)
    userTrip = UserTrips.objects.add(user, trip)
    return redirect('/main')

def addToMyTrips(request, id):
    user = User.objects.get(id=request.session['id'])
    trip = Trips.objects.get(id=id)
    UserTrips.objects.add(user, trip)
    return redirect('/main')

def destination(request, id):
    if "id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')
    trip = Trips.objects.get(id=id)
    user = User.objects.get(id=request.session['id'])
    context = { 'trip' : trip,
                'userTrip' : UserTrips.objects.filter(trip=trip).exclude(user=trip.user )}
    return render(request, 'main/destination.html', context)

def makeChanges(request, id):
    Trips.objects.makeChanges(request.POST, id)
    return redirect('/main')

def delete(request, id):
    Trips.objects.filter(id=id).delete()
    return redirect('/main')

def logout(request):
    request.session.flush()
    return redirect('/')
