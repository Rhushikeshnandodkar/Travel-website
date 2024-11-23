from django.shortcuts import render, redirect
from .models import *
import pandas as pd
import pickle
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import googlemaps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    user = request.user
    places = PlaceMode.objects.all()
    return render(request, 'index.html', {"places" : places[0: 10], 'user': user})

def details(request, pk):
    place = PlaceMode.objects.get(id=pk)
    places_pickle = os.path.join(settings.MEDIA_ROOT, 'movies.pkl')
    similarity_pickle = os.path.join(settings.MEDIA_ROOT, 'similarity.pkl')
        
    place_dict = pickle.load(open(places_pickle, 'rb'))
    similarity = pickle.load(open(similarity_pickle, 'rb'))
    name = place.Name
    place_index = place_dict[place_dict['Name'] == name].index[0]
    distances = similarity[place_index]
    places_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x : x[1])[1:5]
    recommended_places = []
    for i in places_list:
        recommended_places.append(PlaceMode.objects.get(id=i[0]))
    crowd_data = CrowdModel.objects.filter(location=place)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augast', 'September', 'October', 'November', 'December']
    data = []
    reviews = ReviewModel.objects.filter(place=pk)
    return render(request, 'details.html', {"rec_places" : recommended_places, 'single_place' : place, 'crowd_data' : crowd_data, 'months': months, 'reviews':reviews})

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = PlaceMode.objects.filter(
            models.Q(Name__icontains=query) |
            models.Q(City__icontains=query) |
            models.Q(Significance__icontains=query)
        )
    return render(request, 'search.html', {'places': results, 'query': query})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.error(request, 'Username allready exists')
            return redirect('/signup')
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            return redirect('/')
        else:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
    return render(request, 'signup.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # Replace 'home' with your desired redirect URL
        else:
            messages.error(request, 'user does not exists')
            return redirect('/login')
            # return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


gmaps = googlemaps.Client(key="AIzaSyAyUAkmbw3LUmZy5w15DmMFaVh3x-utvHw")
def get_distance(origin, destination):
    """
    Calculate the distance between two locations using Google Maps Distance Matrix API.
    """
    try:
        result = gmaps.distance_matrix(origins=origin, destinations=destination, mode="driving")
        element = result["rows"][0]["elements"][0]
        if element["status"] == "OK":
            distance = element["distance"]["value"]  # Distance in meters
            return distance / 1000  # Convert to kilometers
        else:
            return None
    except Exception as e:
        print(f"Error fetching distance: {e}")
        return None

@csrf_exempt
def estimate_cost(request):
    """
    API to estimate travel cost.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            origin = data.get("origin")
            destination = data.get("destination")

            if not (origin and destination):
                return JsonResponse({"error": "Invalid input"}, status=400)

            # Calculate distance
            distance = get_distance(origin, destination)
            if distance is None:
                return JsonResponse({"error": "Could not fetch distance"}, status=500)

            # Calculate cost (example: ₹10 per km)
            cost = distance * 10

            return JsonResponse({"cost": cost})
        except Exception as e:
            print(f"Error in API: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

