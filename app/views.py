from django.shortcuts import render, redirect
from .models import *
import pandas as pd
import pickle
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
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
    places_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x : x[1])[1:15]
    recommended_places = []
    for i in places_list:
        recommended_places.append(PlaceMode.objects.get(id=i[0]))
    return render(request, 'details.html', {"rec_places" : recommended_places, 'single_place' : place})

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
        
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            return redirect('login')
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
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
