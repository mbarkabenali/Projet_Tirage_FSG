from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_demandes, name='liste_demandes'),
    path('demander/', views.creer_demande, name='creer_demande'),
    path('agent/', views.espace_agent, name='espace_agent'),
    path('agent/statut/<int:demande_id>/<str:nouveau_statut>/', views.changer_statut, name='changer_statut'),
    path('modifier/<int:demande_id>/', views.modifier_demande, name='modifier_demande'),
    path('supprimer/<int:demande_id>/', views.supprimer_demande, name='supprimer_demande'),
    path('demande/<int:demande_id>/', views.detail_demande, name='detail_demande'), 
]