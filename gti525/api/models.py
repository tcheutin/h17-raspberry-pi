from django.db import models

# Create your models here.
class Terminal(models.Model):
    ''' BD local to a PI '''
    CONNECTED = 'Connected'
    NON_RESPONSIVE = 'Non-Responsive'
    CONNECTION_STATUS = ((CONNECTED, 'Connected'),
                         (NON_RESPONSIVE, 'Non-Responsive'))

    id = models.AutoField(primary_key=True)
    status  = models.CharField(max_length=30,
                               choices=CONNECTION_STATUS,
                               default=CONNECTED)
    macAddress = models.CharField(max_length=30)

class Mobile(models.Model):
    ''' BD local to a PI '''
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

class Ticket(models.Model):
    ''' This DB will be shared between the PI '''
    VALIDATED = 'Validated'
    NON_VALIDATED = 'Non-Validated'
    TICKET_STATUS = ((VALIDATED, 'Validated'),
                     (NON_VALIDATED, 'Non-validated'))

    ticketHash = models.CharField(max_length=30, unique=True, default=None)
    status = models.CharField(max_length=30,
                              choices=TICKET_STATUS,
                              default=NON_VALIDATED)
    validationTime = models.DateTimeField()
    validationTerminal = models.ForeignKey(Terminal, null=True)
