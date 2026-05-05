from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from VehiTrack.models import Matricule, Document, HistoriqueDocument


def index(request):
    return render(request, "VehiTrack/index.html")

def liste_matricules(request):
    matricules = Matricule.objects.all()
    return render(request, "VehiTrack/liste.html", {"matricules": matricules})

# Détails d’un matricule et ses documents
def detail_matricule(request, matricule_id):
    matricule = get_object_or_404(Matricule, id=matricule_id)
    documents = matricule.documents.all()
    return render(request, "VehiTrack/detail.html", {"matricule": matricule, "documents": documents})

# Ajouter un document
@login_required
def ajouter_document(request, matricule_id):
    matricule = get_object_or_404(Matricule, id=matricule_id)
    if request.method == "POST":
        titre = request.POST.get("titre")
        contenu = request.POST.get("contenu")
        doc = Document.objects.create(
            matricule=matricule,
            titre=titre,
            contenu=contenu,
            auteur=request.user
        )
        HistoriqueDocument.objects.create(
            document=doc,
            action="création",
            utilisateur=request.user,
            details=f"Document {titre} ajouté"
        )
        return redirect("detail_matricule", matricule_id=matricule.id)
    return render(request, "VehiTrack/ajouter.html", {"matricule": matricule})

# Voir l’historique d’un document
def historique_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    historiques = document.historiques.all().order_by("-date_action")
    return render(request, "VehiTrack/historique.html", {"document": document, "historiques": historiques})
from django.shortcuts import render
from .models import Matricule

def rechercher_documents(request):
    documents = None
    matricule_code = None

    if request.method == "POST":
        matricule_code = request.POST.get("matricule")
        try:
            matricule = Matricule.objects.get(code=matricule_code)
            documents = matricule.documents.all()
        except Matricule.DoesNotExist:
            documents = []

    return render(request, "VehiTrack/recherche.html", {
        "documents": documents,
        "matricule_code": matricule_code
    })
from django.shortcuts import redirect

def supprimer_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    matricule_id = document.matricule.id
    document.delete()
    return redirect("detail_matricule", matricule_id=matricule_id)
from .models import Document

def supprimer_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    matricule_id = document.matricule.id
    document.delete()
    return redirect("detail_matricule", matricule_id=matricule_id)
