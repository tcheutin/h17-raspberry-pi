from django.db import models
from datetime import date

# Create your models here
class Terminal(models.Model):
    ''' Object representation of a Raspberry PI terminal '''
    CONNECTED = 'Connected'
    NON_RESPONSIVE = 'Non-Responsive'
    CONNECTION_STATUS = ((CONNECTED, 'Connected'),
                         (NON_RESPONSIVE, 'Non-Responsive'))

    id = models.AutoField(primary_key=True)
    status  = models.CharField(max_length=30,
                               choices=CONNECTION_STATUS,
                               default=CONNECTED)
    ipAddress = models.CharField(max_length=30, null=True)

class Mobile(models.Model):
    ''' Object representation of a mobile device '''
    CONNECTED = 'Connected'
    NON_RESPONSIVE = 'Non-Responsive'
    CONNECTION_STATUS = ((CONNECTED, 'Connected'),
                         (NON_RESPONSIVE, 'Non-Responsive'))

    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=30)
    ipAddress = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30,
                              choices=CONNECTION_STATUS,
                              default=CONNECTED)
    loginTime = models.DateTimeField(default=date.today)
    logoutTime = models.DateTimeField(null=True)

class Ticket(models.Model):
    ''' Object representation of a event ticket '''
    VALIDATED = 'Validated'
    NON_VALIDATED = 'Non-Validated'
    IN_PROGRESS = 'In Progress'
    TICKET_STATUS = ((VALIDATED, 'Validated'),
                     (NON_VALIDATED, 'Non-Validated'),
                     (IN_PROGRESS, 'In Progress'))

    ticketHash = models.CharField(max_length=30, unique=True, default=None)
    status = models.CharField(max_length=30,
                              choices=TICKET_STATUS,
                              default=NON_VALIDATED)
    validationTime = models.DateTimeField()
    validationTerminal = models.ForeignKey(Terminal, null=True)

class MobileCommLog(models.Model):
    ''' Only used to store the log of ours validations attempts '''
    mobileId = models.ForeignKey(Mobile)
    ticketId = models.ForeignKey(Ticket)
    httpResponse = models.IntegerField()
