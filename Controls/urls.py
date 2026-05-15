"""
URL configuration for Controls project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from VehiTrack import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('VehiTrack.urls')),
    path('', views.index, name='index'),
    path('', views.redirection_apres_connexion, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path("connexion/", auth_views.LoginView.as_view(template_name='vehiTrack/connexion.html'), name="login"),
    path("deconnexion/", auth_views.LoginView.as_view(next_page='acceuil'), name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recherche/', views.rechercher_documents, name='rechercher_documents'),
    path('matricules/', views.liste_matricules, name='liste_matricules'),
    path('matricule/<int:matricule_id>/', views.detail_matricule, name='detail_matricule'),
    path('document/<int:doc_id>/historique/', views.historique_document, name='historique_document'),
    path('matricule/<int:matricule_id>/ajouter/', views.ajouter_document, name='ajouter_document'),
    path('document/<int:doc_id>/supprimer/', views.supprimer_document, name='supprimer_document'),


]