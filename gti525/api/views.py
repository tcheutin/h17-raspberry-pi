from api.models import Terminal, Ticket, MobileCommLog
from api.serializers import TerminalSerializer, TicketSerializer, PublicTicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime
from django.utils import timezone
from api.GridCommunication import TerminalControler
from django.core.exceptions import ObjectDoesNotExist
import manage as main

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
        if main.have_receive_ticket:
            # This code was taken here: http://stackoverflow.com/a/4581997
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            ##############################################################
            try:
                terminal = Terminal.objects.get(ipAddress=ip)
                if terminal.status == 'Non-Responsive':
                    terminal.status = 'Connected'
                    terminal.save()
            except ObjectDoesNotExist:
                terminal = Terminal(ipAddress=ip, status='Connected')
                terminal.save()
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)
        else:
            return Response({'NotReady': 'True'})

class TicketValidation(APIView):
    ''' Retrieve or update a ticket. '''

    def httpCodeToValidationStatus(self, httpCode):
        if httpCode == 202:
            return 'Validated'
        elif httpCode == 404:
            return 'Invalid Ticket'
        elif httpCode == 409:
            return 'Ticket Already Validated'
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
        MobileCommLog.objects.create(ticketHash=ticket.ticketHash, httpResponse=httpResponse, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return Response(payload, status=httpResponse)

    def patch(self, request, ticketHash, format=None):
        # This code was taken here: http://stackoverflow.com/a/4581997
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        ##############################################################
        try:
            terminal = Terminal.objects.get(ipAddress=ip)
            if terminal.status == 'Non-Responsive':
                terminal.status = 'Connected'
                terminal.save()
        except ObjectDoesNotExist:
            terminal = Terminal(ipAddress=ip, status='Connected')
            terminal.save()

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
