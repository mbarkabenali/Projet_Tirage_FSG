from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import DemandeTirageForm 
from .models import DemandeTirage, Enseignant

@login_required
def liste_demandes(request):
    enseignant_profile = get_object_or_404(Enseignant, user=request.user)
    demandes = DemandeTirage.objects.filter(enseignant=enseignant_profile)
    return render(request, 'core/liste_demandes.html', {'demandes': demandes})

@login_required
def creer_demande(request):
    enseignant_profile = get_object_or_404(Enseignant, user=request.user)

    if request.method == 'POST':
        form = DemandeTirageForm(request.POST, request.FILES)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.enseignant = enseignant_profile
            
            deja_reserve = DemandeTirage.objects.filter(
                date_reservation=demande.date_reservation,
                heure_debut=demande.heure_debut
            ).exists()
            
            if deja_reserve:
                messages.error(request, "Ce créneau horaire est déjà réservé ! Veuillez en choisir un autre.")
            else:
                demande.save()
                messages.success(request, "Réservation effectuée avec succès !")
                return redirect('liste_demandes')
    else:
        form = DemandeTirageForm()
    
    return render(request, 'core/creer_demande.html', {'form': form})

@staff_member_required
def espace_agent(request):
    demandes = DemandeTirage.objects.all().order_by('-id')

    # Récupération des paramètres de recherche/filtre
    query = request.GET.get('q', '')
    statut_filter = request.GET.get('statut', '')

    # Filtre par terme de recherche (matiere ou username de l'enseignant)
    if query:
        demandes = demandes.filter(
            matiere__icontains=query
        ) | demandes.filter(
            enseignant__user__username__icontains=query
        )

    # Filtre par statut
    if statut_filter:
        demandes = demandes.filter(statut=statut_filter)

    context = {
        'demandes': demandes,
        'query': query,
        'statut_filter': statut_filter,
    }
    return render(request, 'core/espace_agent.html', context)

@staff_member_required
def changer_statut(request, demande_id, nouveau_statut):
    demande = get_object_or_404(DemandeTirage, id=demande_id)
    demande.statut = nouveau_statut
    demande.save()
    
    messages.success(request, f"Le statut de la demande #{demande.id} a été mis à jour en '{nouveau_statut}'.")
    return redirect('espace_agent')

@login_required
def modifier_demande(request, demande_id):
    enseignant_profile = get_object_or_404(Enseignant, user=request.user)
    demande = get_object_or_404(DemandeTirage, id=demande_id, enseignant=enseignant_profile)

    # Sécurité : vérifier que la demande est bien en attente
    if demande.statut != 'EN_ATTENTE' and demande.statut != 'En attente':
        messages.error(request, "Impossible de modifier une demande déjà prise en charge.")
        return redirect('liste_demandes')

    if request.method == 'POST':
        form = DemandeTirageForm(request.POST, request.FILES, instance=demande)
        if form.is_valid():
            form.save()
            messages.success(request, "Demande modifiée avec succès !")
            return redirect('liste_demandes')
    else:
        form = DemandeTirageForm(instance=demande)

    return render(request, 'core/modifier_demande.html', {'form': form, 'demande': demande})


@login_required
def supprimer_demande(request, demande_id):
    enseignant_profile = get_object_or_404(Enseignant, user=request.user)
    demande = get_object_or_404(DemandeTirage, id=demande_id, enseignant=enseignant_profile)

    if demande.statut == 'EN_ATTENTE' or demande.statut == 'En attente':
        demande.delete()
        messages.success(request, "Demande annulée et supprimée avec succès.")
    else:
        messages.error(request, "Impossible d'annuler une demande déjà en cours ou terminée.")

    return redirect('liste_demandes')

@login_required
def detail_demande(request, demande_id):
    # Si c'est un agent/staff, il a accès à toutes les demandes. Sinon, seulement ses propres demandes.
    if request.user.is_staff or request.user.is_superuser:
        demande = get_object_or_404(DemandeTirage, id=demande_id)
    else:
        enseignant_profile = get_object_or_404(Enseignant, user=request.user)
        demande = get_object_or_404(DemandeTirage, id=demande_id, enseignant=enseignant_profile)
        
    return render(request, 'core/detail_demande.html', {'demande': demande})