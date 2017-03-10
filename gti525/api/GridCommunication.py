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
        headers = {'api-Key': 'bob'}
        for terminal in terminals:
            if terminal.status == 'Connected':
                url = 'http://'+terminal.ipAddress+':8000/api/ticket/'+ticketHash+'/'
                print('Request GET: '+url)
                try:
                    response = requests.get(url, headers=headers, timeout=1)
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
                except requests.exceptions.Timeout:
                    terminal.status = 'Non-Responsive'
                    terminal.save()
                    print('TIMEOUT')
        return isAlreadyValidated

    def validateTicket(self, ticketHash):
        terminals = Terminal.objects.all()
        headers = {'api-Key': 'bob'}
        for terminal in terminals:
            if terminal.status == 'Connected':
                url = 'http://'+terminal.ipAddress+':8000/api/ticket/validate/'+ticketHash+'/'
                print('Request PATCH: '+url)
                try:
                    response = requests.patch(url, headers=headers, timeout=1)
                except requests.exceptions.Timeout:
                    terminal.status = 'Non-Responsive'
                    terminal.save()
                    print('TIMEOUT')

    def run(self):
        time.sleep(3) #To let te server start before sending a request to it
        ticketValidated = self.verifyTicketValidation('12345abcdef')
        print('Ticket was already validated: '+str(ticketValidated))
        if not ticketValidated :
            self.validateTicket('12345abcdef')

    def launch(self):
        self.run()
