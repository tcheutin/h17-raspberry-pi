from api.models import Terminal, Ticket, Mobile
from api.serializers import TerminalSerializer, TicketSerializer, PublicTicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime
from django.utils import timezone

class TerminalList(APIView):
    ''' List all terminal or create a new terminal. '''

    def get(self, request, format=None):
        terminals = Terminal.objects.all()
        serializer = TerminalSerializer(terminals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TerminalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketList(APIView):
    ''' List all ticket. '''

    def get(self, request, format=None):
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)

class TicketDetail(APIView):
    ''' Retrieve or update a ticket. '''

    def get_object(self, ticketHash):
        try:
            return Ticket.objects.get(ticketHash=ticketHash)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request, ticketHash, format=None):
        ticket = self.get_object(ticketHash)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, ticketHash, format=None):
        ticket = self.get_object(ticketHash)
        if ValidationControler.isValidated(ticket):
            content = {'detail': 'ticket already validated'}
            return Response(content, status=status.HTTP_409_CONFLICT)
        ticket.validationTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ticket.status = 'Validated'
        serializer = PublicTicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidationControler():
    def isValidated(ticket):
        return ticket.status == "Validated"
