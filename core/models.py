from django.db import models
from django.contrib.auth.models import User

class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departement = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class DemandeTirage(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours d impression'),
        ('TERMINE', 'Terminé'),
        ('REFUSE', 'Refusé'),
    ]

    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    matiere = models.CharField(max_length=100)
    titre_epreuve = models.CharField(max_length=200)
    nombre_exemplaires = models.PositiveIntegerField()
    nombre_pages = models.PositiveIntegerField()
    fichier_pdf = models.FileField(upload_to='epreuves_pdf/')
    filiere = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)
    
    date_reservation = models.DateField()
    heure_debut = models.TimeField()
    duree_minutes = models.PositiveIntegerField(default=15)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    date_demande = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Formule : 5 min de base + 2 min par tranche de 100 impressions (copies * pages)
        total_pages = self.nombre_exemplaires * self.nombre_pages
        self.duree_minutes = 5 + (total_pages // 100) * 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre_epreuve} - {self.enseignant.user.username}"