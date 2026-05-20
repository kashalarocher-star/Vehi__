from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Matricule

class InscriptionForm(UserCreationForm):
    matricule = forms.CharField(max_length=50, label="Matricule du vehicule")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def clean_matricule(self):
        code = self.cleaned_data['matricule']
        try:
            self.matricule_instance = Matricule.objects.get(code=code)
        except Matricule.DoesNotExist:
            raise forms.ValidationError("Ce matricule n'existe pas dans notre base.")
        # Vérifier si le matricule a déjà un propriétaire
        if self.matricule_instance.proprietaire is not None:
            raise forms.ValidationError("Ce véhicule est déjà associé à un compte.")
        return code
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['matricule']
        user.email = self.cleaned_data['email']
        # Nouvel utilisateur = simple (non staff)
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
            #associe l'utilisateur au matricule
            self.matricule_instance.proprietaire = user
            self.matricule_instance.save()
        return user