from django.db import models
from datetime import date

# Create your models here
class Terminal(models.Model):
    CONNECTION_STATUS = (('c', 'Connected'),
                         ('n', 'Non-Responsive'))

    id = models.AutoField(primary_key=True)
    status  = models.CharField(max_length=30,
                               choices=CONNECTION_STATUS,
                               default='c')
    ipAddress = models.CharField(max_length=30, default='')

class Mobile(models.Model):
    CONNECTION_STATUS = (('c', 'Connected'),
                         ('n', 'Non-Responsive'))

    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=30, default='')
    ipAddress = models.CharField(max_length=30, default='')
    status = models.CharField(max_length=30,
                              choices=CONNECTION_STATUS,
                              default='c')
    loginTime = models.DateTimeField(default=date.today)
    logoutTime = models.DateTimeField(null=True)

class Auditorium(models.Model):
    name = models.CharField(max_length=30, default='')
    address = models.CharField(max_length=30, default='')

class Event(models.Model):
    name = models.CharField(max_length=30, default='')
    time = models.DateTimeField(null=True)
    auditorium = models.ForeignKey(Auditorium, null=True)


class Ticket(models.Model):
    TICKET_STATUS = (('v', 'Validated'),
                     ('n', 'Non-Validated'),
                     ('i', 'In Progress'))

    ticketHash = models.CharField(max_length=30, unique=True, default=None)
    status = models.CharField(max_length=30,
                              choices=TICKET_STATUS,
                              default='n')
    validationTime = models.DateTimeField(null=True)
    validationTerminal = models.ForeignKey(Terminal, null=True)
    owner = models.CharField(max_length=30, default='')
    event = models.ForeignKey(Event, null=True)

class MobileCommLog(models.Model):
    ''' Only used to store the log of ours validations attempts '''
    mobileId = models.ForeignKey(Mobile)
    ticketId = models.ForeignKey(Ticket)
    httpResponse = models.IntegerField()
