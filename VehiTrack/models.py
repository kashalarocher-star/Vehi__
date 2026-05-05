from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Matricule(models.Model):
    code = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Document(models.Model):
    matricule = models.ForeignKey(Matricule, on_delete=models.CASCADE, related_name="documents")
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.ImageField(upload_to="documents/", blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.titre} ({self.matricule.code})"
class HistoriqueDocument(models.Model):
    document = models.ForeignKey("Document", on_delete=models.CASCADE, related_name="historiques")
    action = models.CharField(max_length=50)  # création, modification, suppression
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_action = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} - {self.document.titre} ({self.date_action})"