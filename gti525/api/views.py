from api.models import Terminal, Ticket, MobileCommLog
from api.serializers import TerminalSerializer, TicketSerializer, PublicTicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime
from django.utils import timezone
from api.GridCommunication import TerminalControler

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

class TicketValidation(APIView):
    ''' Retrieve or update a ticket. '''

    def httpCodeToValidationStatus(self, httpCode):
        if httpCode == 202:
            return 'Validated'
        elif httpCode == 404:
            return 'Invalid Ticket'
        elif httpCode == 409:
            return 'Ticekt Already Validated'
        else:
            return 'INVALID HTTP CODE'

    def get_object(self, ticketHash):
        try:
            return Ticket.objects.get(ticketHash=ticketHash)
        except Ticket.DoesNotExist:
            raise Http404

    def isValidated(selft,ticket):
        return ticket.status == "Validated"

    def get(self, request, ticketHash, format=None):
        ticket = self.get_object(ticketHash)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, ticketHash, format=None):
        payload = ''
        httpResponse = ''
        ticket = self.get_object(ticketHash)
        logValidation = ''
        if self.isValidated(ticket):
            payload = {'detail': 'ticket already validated'}
            httpResponse = status.HTTP_409_CONFLICT
        else:
            if TerminalControler().verifyTicketValidation(ticketHash):
                payload = {'detail': 'ticket already validated'}
                httpResponse = status.HTTP_409_CONFLICT
                ticket.status = 'Validated'
                serializer = PublicTicketSerializer(ticket, data=request.data)
                if serializer.is_valid():
                    serializer.save()
            else:
                TerminalControler().validateTicket(ticketHash)
                ticket.validationTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ticket.status = 'Validated'
                serializer = PublicTicketSerializer(ticket, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    payload = serializer.data
                    httpResponse = status.HTTP_202_ACCEPTED
                else:
                    payload = serializers.errors
                    httpResponse = status.HTTP_400_BAD_REQUEST
        status = self.httpCodeToValidationStatus(httpResponse)
        MobileCommLog.objects.create(ticketHash=ticket.ticketHash, httpResponse=status, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return Response(payload, status=httpResponse)

    def patch(self, request, ticketHash, format=None):
        payload = ''
        httpResponse = ''
        ticket = self.get_object(ticketHash)
        if self.isValidated(ticket):
            payload = {'detail': 'ticket already validated'}
            httpResponse = status.HTTP_409_CONFLICT
        else:
            ticket.validationTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ticket.status = 'Validated'
            serializer = PublicTicketSerializer(ticket, data=request.data)
            if serializer.is_valid():
                serializer.save()
                payload = serializer.data
                httpResponse = status.HTTP_202_ACCEPTED
            else:
                payload = serializers.errors
                httpResponse = status.HTTP_400_BAD_REQUEST
        return Response(payload, status=httpResponse)
