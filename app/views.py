from django.shortcuts import render
from .models import *
import pandas as pd
import pickle
import os
from django.conf import settings
# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        places = PlaceMode.objects.filter(Name=name)
    places = PlaceMode.objects.all()
    return render(request, 'index.html', {"places" : places})

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