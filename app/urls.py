from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('form/', views.basic, name='basic'),
    path('trait/', views.trait, name='traitement'),
    path('graphes/', views.graphes, name='graphiques'),
    path('wordcloud/', views.wordcloud, name='WordCloud'),
]
