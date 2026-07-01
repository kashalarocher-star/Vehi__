from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date, timedelta

class Matricule(models.Model):
    #ajouter les types de vehicule
    TYPE_VEHICULE_CHOICES =[
        ('camionnette', 'Camionnette'),
        ('suv', 'Suv'),
        ('camion', 'Camion'),
        ('voiture', 'Voiture'),
        ('autre', 'Autre'),
    ]
    type_vehicule = models.CharField(max_length=20, choices=TYPE_VEHICULE_CHOICES, null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicule', null=True, blank=True)
    def __str__(self):
        return f"{self.code} - {self.nom}"

    class Meta:
        app_label = 'VehiTrack'
class Document(models.Model):
    TYPE_CHOICES = [
        ('assurence', 'Assurence'),
        ('visite_technique', 'Visite_technique'),
        ('carte_grise', 'Carte_grise'),
        ('autre', 'Autre'),

    ]
    TYPE_CHOICE = [
        ('carte rose', 'carte rose'),
        ('permis de conduire', 'permis de conduire'),
        ('assurence', 'assurence'),
        ('controle technique', 'controle technique'),
        ('stationnement', 'stationnement'),
        ('vignette', 'vignette'),
        ('autorisation de transport(patente)', 'autorisation de transport(patente)'),
    ]
    plaque_d_immatricule = models.ForeignKey(Matricule, on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    titre = models.CharField(max_length=200, choices=TYPE_CHOICE,default='titre du document')
    contenu_du_document = models.TextField()
    image = models.ImageField(upload_to="documents/", blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type_document = models.CharField(max_length=50, choices=TYPE_CHOICE,default='carte rose')
    date_expiration = models.DateField(null=True, blank=True, help_text="Date d'expiration")

    @property
    def statut(self):
        if not self.date_expiration:
            return 'inconnu'
        aujourdhui = date.today()
        if self.date_expiration < aujourdhui:
            return 'expirer'
        elif self.date_expiration <= aujourdhui + timedelta(days=30):
            return 'expire_bientôt'
        return 'valide'
    
    def __str__(self):
        if self.plaque_d_immatricule:
            return f"{self.titre} ({self.plaque_d_immatricule.code})"
        return f"{self.titre} (⚠️ faut mettre une plaque)"
    class Meta:
        app_label = 'VehiTrack'
class HistoriqueDocument(models.Model):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="historiques")
    action = models.CharField(max_length=50)  # création, modification, suppression 
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.document.titre} ({self.date_action})"
    class Meta:
        app_label = 'VehiTrack'