from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
# Create your models here.


def validate_letters(value):
    if not re.match(r'^[A-Za-z]+$', value):
        raise ValidationError('this field should contain only letters')


class Categorie(models.Model):
    # hedhi verification nekho ken des lettres, message d'erreur
    letters_only = RegexValidator(r'^[A-Za-z]+$', 'only letters are allowed')
    #title = models.CharField(max_length=255, validators=[letters_only])
    title = models.CharField(max_length=255, validators=[validate_letters])
    create_at = models.DateTimeField(auto_now_add=True)  # table de creation
    update_tat = models.DateTimeField(auto_now=True)  # date sys

    class Meta:
        verbose_name_plural = "Categories"
