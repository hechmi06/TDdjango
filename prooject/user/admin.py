
from django.contrib import admin
from .models import participant
from .models import Reservation
# Register your models here.
admin.site.register(participant)
admin.site.register(Reservation)
