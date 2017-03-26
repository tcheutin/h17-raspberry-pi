from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Terminal, Ticket, Auditorium, Event, MobileCommLog

class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = ('name', 'address')

class EventSerializer(serializers.ModelSerializer):
    auditorium = AuditoriumSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ('name', 'time', 'auditorium')

class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        fields = ('ipAddress', 'status')

class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ('ticketHash', 'owner', 'status',
                  'validationTime', 'event')

class PublicTicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ('ticketHash', 'owner' ,'status', 'event')
        read_only_fields = ('ticketHash', 'owner' ,'status', 'event')

class ValidationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileCommLog
        fields = ('ticketHash', 'httpResponse' ,'time')
        read_only_fields = ('ticketHash', 'httpResponse' ,'time')
