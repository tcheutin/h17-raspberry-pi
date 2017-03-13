from django.db import models
from datetime import date

class Terminal(models.Model):
    CONNECTION_STATUS = (('Connected', 'Connected'),
                         ('Non-Responsive', 'Non-Responsive'))

    id = models.AutoField(primary_key=True)
    status  = models.CharField(max_length=30,
                               choices=CONNECTION_STATUS,
                               default='Connected')
    ipAddress = models.CharField(max_length=30, default='')

class Auditorium(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, default='')
    address = models.CharField(max_length=30, default='')

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, default='')
    time = models.DateTimeField(null=True)
    auditorium = models.ForeignKey(Auditorium, null=True)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    TICKET_STATUS = (('Validated', 'Validated'),
                     ('Non-Validated', 'Non-Validated'),
                     ('In Progress', 'In Progress'))

    ticketHash = models.CharField(max_length=30, default=None)
    status = models.CharField(max_length=30,
                              choices=TICKET_STATUS,
                              default='Non-Validated')
    validationTime = models.DateTimeField(null=True)
    owner = models.CharField(max_length=30, default='')
    event = models.ForeignKey(Event, null=True)

class MobileCommLog(models.Model):
    ''' Only used to store the log of ours validations attempts '''
    id = models.AutoField(primary_key=True)
    ticketHash = models.CharField(max_length=30, default='')
    httpResponse = models.CharField(max_length=30, default='')
    time = models.DateTimeField(null=True)
