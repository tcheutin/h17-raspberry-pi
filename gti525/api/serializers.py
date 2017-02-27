from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Terminal, Mobile, Ticket, Auditorium, Event

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
    validationTerminal = TerminalSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ('ticketHash', 'owner', 'status',
                  'validationTime', 'validationTerminal', 'event')

class PublicTicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = ('ticketHash', 'owner' ,'status', 'event')
        read_only_fields = ('ticketHash', 'event', 'owner')