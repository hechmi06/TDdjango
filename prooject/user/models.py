from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from conferences.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def emailValidator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('Email invalide ....')


class participant(AbstractUser):
   
    cin = models.CharField(primary_key=True, max_length=8, validators=[cin_valid])
    email = models.CharField(unique=True, max_length=255, validators=[emailValidator])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'username'
    CHOICES = (
        ('etudiant', 'etudiant'),
        ('chercheur', 'chercheur'),
        ('doctuer', 'docteur'),
        ('enseignant', 'enseigant')
    )
    participant_categorie = models.CharField(max_length=255, choices=CHOICES)
    reservations = models.ManyToManyField(Conference, through='Reservation', related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Participants"


class Reservation(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    participant = models.ForeignKey(participant, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    Reservation_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.conference.start_date < timezone.now().date():
            raise ValidationError("you can only reseve for upcoming")
        reservationCount = Reservation.objects.filter(
            participant=self.participant,
            reservation_date=self.Reservation_date
        )
        if reservationCount > 3:
            raise ValidationError("you only can make up to  reservations")

    class Meta:
        verbose_name_plural = "Reservations"
        unique_together = ('conference', 'participant')
