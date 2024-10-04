from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('details/<int:pk>/', views.details, name="details"),
    path('search', views.search_view, name='search')
    # path('', include('app.urls'))
]
