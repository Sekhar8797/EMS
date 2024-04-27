from django.db import models



class Organizer(models.Model):
    organizer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    phone_number = models.CharField(default="")
    password = models.CharField(max_length=100, default='user')

    def _str_(self):
        return self.name


class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    phone_number = models.CharField(default="")
    password = models.CharField(max_length=100, default='user')

    def _str_(self):
        return self.name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    count = models.IntegerField(default=0)
    org_id = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    def _str_(self):
        return self.name


from django.db import models
from django.utils import timezone


from django.db import models
from django.utils import timezone

class Registration(models.Model):
    class RegistrationStatus(models.TextChoices):
        REGISTERED = 'registered', 'Registered'
        UNREGISTERED = 'unregistered', 'Unregistered'

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=12,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.REGISTERED,
    )

    def __str__(self):
        return f'{self.participant.name} registered for {self.event.name}: {self.status}'
