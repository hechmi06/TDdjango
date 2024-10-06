from django.db import models
from categories.models import Categorie
from django.core.validators import MaxValueValidator, FileExtensionValidator
# Create your models here.
from django.utils import timezone
from django.core.exceptions import ValidationError


class Conference(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now().date())
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(validators=[MaxValueValidator(limit_value=50, message="rak khit fih")])
    program = models.FileField(
        upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'], message="only pdf")])

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="Conferences")  # on_delete ajouté
    # related_name : bech tnejem todkhol lel a partir mel categorie lel conference

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('end date must be greater than start date')

    class Meta:
        verbose_name_plural = "Conferences"
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=timezone.now().date()  # start_date >= datesystem
                ),
                name="the start date must be greater or equal then system date "
            )
        ]
