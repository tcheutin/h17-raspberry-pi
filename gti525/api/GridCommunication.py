from api.models import Terminal, Ticket, Auditorium, Event
import requests
import time
import netifaces as ni
from api.serializers import TicketSerializer
from io import StringIO
from rest_framework.parsers import JSONParser


class TerminalControler():

    def obtainTicketList(self, ipAddress):
        try:
            tickets = Ticket.objects.all()
            auditoriums = Auditorium.objects.all()
            events = Event.objects.all()
            url = 'http://'+ipAddress+':8000/api/tickets/'
            headers = {'api-Key': 'bob'}
            print('GET: '+url)
            response = requests.get(url, headers=headers, timeout=2)
            tickets_dict = response.json()
            for ticket_dict in tickets_dict:
                ticketHash = ticket_dict.get('ticketHash')
                owner = ticket_dict.get('owner')
                ticket_status = ticket_dict.get('status')
                validationTime = ticket_dict.get('validationTime')
                event_dict = ticket_dict.get('event')

                event_name = event_dict.get('name')
                event_time = event_dict.get('time')
                auditorium_dict = event_dict.get('auditorium')

                auditorium_name = auditorium_dict.get('name')
                auditorium_address = auditorium_dict.get('address')

                auditorium = Auditorium(name=auditorium_name, address=auditorium_address)
                for audi in auditoriums:
                    if audi.name == auditorium_name and audi.address == auditorium_address:
                        auditorium = audi
                auditorium.save()

                event = Event(name=event_name, time=event_time, auditorium=auditorium)
                for ev in events:
                    if ev.name == event_name:
                        event = ev
                event.save()

                ticket = Ticket(ticketHash=ticketHash, status=ticket_status,
                                validationTime=validationTime, owner=owner, event=event)
                for tick in tickets:
                    if tick.ticketHash == ticketHash:
                        ticket = tick
                ticket.save()
        except requests.exceptions.Timeout:
            print('TIMEOUT INTERNAL OBTAIN TICKET LIST')

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
                        print('Serializer is not valid:')
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

    def obtainTerminalsFromGestionWebsite(self):
        headers = {'api-Key': 'a677abfcc88c8126deedd719202e50922'}
        url = 'https://gti525-gestionnaire-salle.herokuapp.com/api/terminals/'
        try:
            print('GET: '+url)
            response = requests.get(url, headers=headers, timeout=2)
            f = open('log', 'w')
            f.write(response.text)
            f.close()
            terminals_dict = response.json()
            for terminal_entry in terminals_dict:
                status = terminal_entry.get('status')
                address = terminal_entry.get('address')
                terminal = Terminal(status=status, address=address)
                termianl.save()
        except requests.exceptions.Timeout:
            print('TIMEOUT: OBTAIN TERMINAL LIST')
        except ValueError:
            print('INVALID JSON FORMAT')
            print(response.text)


    def obtainTicketsFromGestionWebsite(self):
        headers = {'api-Key': 'a677abfcc88c8126deedd719202e50922'}
        url = 'https://gti525-gestionnaire-salle.herokuapp.com/api/tickets/'
        try:
            print('GET: '+url)
            response = requests.get(url, headers=headers, timeout=3)
            f = open('log', 'w')
            f.write(response.text)
            f.close()
            tickets_dict = response.json()
            for ticket_dict in tickets_dict:
                ticketHash = ticket_dict.get('id')
                owner = ticket_dict.get('owner')
                event_dict = ticket_dict.get('event')

                event_name = event_dict.get('name')
                event_time = event_dict.get('time')
                auditorium_dict = event_dict.get('auditorium')

                auditorium_name = auditorium_dict.get('name')
                auditorium_address = auditorium_dict.get('address')

                auditorium = Auditorium(name=auditorium_name, address=auditorium_address)
                for audi in auditoriums:
                    if audi.name == auditorium_name and audi.address == auditorium_address:
                        auditorium = audi
                auditorium.save()

                event = Event(name=event_name, time=event_time, auditorium=auditorium)
                for ev in events:
                    if ev.name == event_name:
                        event = ev
                event.save()

                ticket = Ticket(ticketHash=ticketHash, owner=owner, event=event)
                for tick in tickets:
                    if tick.ticketHash == ticketHash:
                        ticket = tick
                ticket.save()
        except requests.exceptions.Timeout:
            print('TIMEOUT: OBTAIN TICKET LIST')
        except ValueError:
            print('INVALID JSON FORMAT')
            print(response.text)

    def sendIPtoGestionWebsite(self, ipAddress):
        headers = {'api-Key': 'a677abfcc88c8126deedd719202e50922'}
        url = 'https://gti525-gestionnaire-salle.herokuapp.com/api/terminals/'
        payload = {'address': ipAddress}
        try:
            print('POST: '+url+' | Payload: '+str(payload))
            response = requests.post(url, headers=headers, timeout=2, data=payload)
            f = open('log', 'w')
            f.write(response.text)
            f.close()
        except requests.exceptions.Timeout:
            print('TIMEOUT: POST IP ADDRESS')

    def run(self):
        time.sleep(3) #To let te server start before sending a request to it
        try:
            config_file = open('interface.config', 'r')
            interface = config_file.readline()
            interface = interface[:-1]
            config_file.close()
        except FileNotFoundError:
            interface = 'eth0'
        ni.ifaddresses(interface)
        ip = ni.ifaddresses(interface)[2][0]['addr']
        print('Local IP Address for '+interface+': '+ip)

        # Query Gestion website for the terminal list
        self.obtainTerminalsFromGestionWebsite()
        # Post to Gestion website our ip address
        self.sendIPtoGestionWebsite(ip)
        # IF no terminal in DB Query Gestion website for ticketsList
        terminals = Terminal.objects.raw('SELECT * FROM api_terminal WHERE "status"="Connected"')
        if len(list(terminals)) == 0:
            self.obtainTicketsFromGestionWebsite()
        # Else Query first PI in the list for the tickets
        else:
            self.obtainTicketList(ipAddress=terminals[0].ipAddress)

    def launch(self):
        self.run()
