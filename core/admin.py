from django.contrib import admin
from .models import Enseignant, DemandeTirage

@admin.register(DemandeTirage)
class DemandeTirageAdmin(admin.ModelAdmin):
    list_display = ('titre_epreuve', 'enseignant', 'statut', 'date_demande')
    list_filter = ('statut', 'filiere')
    search_fields = ('titre_epreuve', 'matiere')
@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    list_display = ('user', 'departement')