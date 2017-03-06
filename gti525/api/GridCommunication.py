from api.models import Terminal, Ticket
import requests
import time
from api.serializers import TicketSerializer
from io import StringIO
from rest_framework.parsers import JSONParser


class TerminalControler():

    def verifyTicketValidation(self, ticketHash):
        isAlreadyValidated = False
        terminals = Terminal.objects.all()
        headers = {'api-Key': 'phahsh1aif5seeth1taeGhahgho6aeNohceijeek4Phaej2ohx'}
        for terminal in terminals:
            url = 'http://'+terminal.ipAddress+':8000/api/ticket/'+ticketHash+'/'
            print('Request GET: '+url)
            response = requests.get(url, headers=headers)
            tickets = response.json()
            serializer = TicketSerializer(data=tickets)
            if serializer.is_valid():
                ticket = serializer.data
                if ticket.get('status') == 'Validated':
                    isAlreadyValidated = True
            else:
                print('FUCK serializer is not valid:')
                for error in serializer.errors:
                    print('Error: '+error)
        return isAlreadyValidated

    def validateTicket(self, ticketHash):
        terminals = Terminal.objects.all()
        headers = {'api-Key': 'phahsh1aif5seeth1taeGhahgho6aeNohceijeek4Phaej2ohx'}
        for terminal in terminals:
            url = 'http://'+terminal.ipAddress+':8000/api/ticket/validate/'+ticketHash+'/'
            print('Request PATCH: '+url)
            response = requests.patch(url, headers=headers)

    def run(self):
        time.sleep(3) #To let te server start before sending a request to it
        ticketValidated = self.verifyTicketValidation('12345abcdef')
        print('Ticket was already validated: '+str(ticketValidated))
        if not ticketValidated :
            self.validateTicket('12345abcdef')

    def launch(self):
        self.run()
