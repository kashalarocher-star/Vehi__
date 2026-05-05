from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('matricules/', views.liste_matricules, name='liste_matricules'),
    
]