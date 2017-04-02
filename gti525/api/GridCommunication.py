from api.models import Terminal, Ticket, Auditorium, Event, MobileCommLog
import requests
import time
import netifaces as ni
from api.serializers import TicketSerializer
from io import StringIO
from rest_framework.parsers import JSONParser
from api.serializers import ValidationLogSerializer
from rest_framework.renderers import JSONRenderer
from django.db import connection
import json
import time
from shutil import copyfile
from datetime import datetime


class TerminalControler():
    headers = {'api-Key': 'a677abfcc88c8126deedd719202e50922'}
    heroku_url = 'https://gti525-gestionnaire-salle.herokuapp.com/api/'


    def obtainTicketList(self, ipAddress):
        try:
            tickets = Ticket.objects.all()
            auditoriums = Auditorium.objects.all()
            events = Event.objects.all()
            url = 'http://'+ipAddress+':8000/api/tickets/'
            print('GET: '+url)
            response = requests.get(url, headers=self.headers, timeout=2)
            f = open('log/GET_TICKET_LIST_INTERNAL.log', 'w')
            f.write('GET: '+ url+'\nResponse\n')
            f.write(response.text)
            f.close()
            tickets_dict = response.json()
            audi_do_not_exist = True
            event_do_not_exist = True
            if tickets_dict:
                for ticket_dict in tickets_dict:
                    tickets = Ticket.objects.all()
                    auditoriums = Auditorium.objects.all()
                    events = Event.objects.all()

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
                    for audi_in_db in auditoriums:
                        if audi_in_db.name == auditorium_name and audi_in_db.address == auditorium_address:
                            audi_do_not_exist = False
                            auditorium = audi_in_db
                            break
                    if audi_do_not_exist:
                        auditorium.save()

                    event = Event(name=event_name, time=event_time, auditorium=auditorium)
                    for event_in_db in events:
                        if event_in_db.name == event_name:
                            event_do_not_exist = False
                            event = event_in_db
                            break
                    if event_do_not_exist:
                        event.save()

                    ticket = Ticket(ticketHash=ticketHash, status=ticket_status,
                                    validationTime=validationTime, owner=owner, event=event)
                    for tick in tickets:
                        if tick.ticketHash == ticketHash:
                            ticket = tick
                    ticket.save()
            else:
                print('Received: No event found retry in 1 sec')
                time.sleep(1)
        except requests.exceptions.Timeout:
            print('TIMEOUT INTERNAL OBTAIN TICKET LIST')

    def verifyTicketValidation(self, ticketHash):
        isAlreadyValidated = False
        terminals = Terminal.objects.all()
        for terminal in terminals:
            if terminal.status == 'Connected':
                url = 'http://'+terminal.ipAddress+':8000/api/ticket/'+ticketHash+'/'
                print('Request GET: '+url)
                try:
                    response = requests.get(url, headers=self.headers, timeout=1)
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
        for terminal in terminals:
            if terminal.status == 'Connected':
                url = 'http://'+terminal.ipAddress+':8000/api/ticket/validate/'+ticketHash+'/'
                print('Request PATCH: '+url)
                try:
                    response = requests.patch(url, headers=self.headers, timeout=1)
                except requests.exceptions.Timeout:
                    terminal.status = 'Non-Responsive'
                    terminal.save()
                    print('TIMEOUT')

    def obtainTerminalsFromGestionWebsite(self, ip):
        url = self.heroku_url+'terminals/'
        headers = self.headers
        headers['ipAddress'] = ip
        try:
            print('GET: '+url)
            response = requests.get(url, headers=headers, timeout=2)
            f = open('log/GET_TERMINAL_LIST.log', 'w')
            f.write('POST: '+url+' | Headers: '+str(headers))
            f.write('\nResponse: \n')
            f.write(response.text)
            f.close()
            terminals_dict = response.json()
            for terminal_entry in terminals_dict:
                status = 'Connected'
                address = terminal_entry.get('address')
                if ip != address:
                    terminal = Terminal(status=status, ipAddress=address)
                    terminal.save()
            return True
        except requests.exceptions.Timeout:
            print('TIMEOUT: OBTAIN TERMINAL LIST')
            return False
        except ValueError:
            print('INVALID JSON FORMAT')
            print(response.text)
            return False


    def obtainTicketsFromGestionWebsite(self, ip):
        url = self.heroku_url+'tickets/'
        headers = self.headers
        headers['ipAddress'] = ip
        try:
            tickets = Ticket.objects.all()
            auditoriums = Auditorium.objects.all()
            events = Event.objects.all()
            print('GET: '+url)
            response = requests.get(url, headers=self.headers, timeout=10)
            f = open('log/GET_TICKET_LIST_GESTION.log', 'w')
            f.write('GET: '+ url+' | Headers: '+str(headers)+'\nResponse\n')
            f.write(response.text)
            f.close()
            tickets_dict = response.json()
            audi_do_not_exist = True
            event_do_not_exist = True
            if not isinstance(tickets_dict, str) :
                for ticket_dict in tickets_dict:
                    tickets = Ticket.objects.all()
                    auditoriums = Auditorium.objects.all()
                    events = Event.objects.all()

                    ticketHash = ticket_dict.get('id')
                    owner = ticket_dict.get('owner')
                    ticket_status = 'Non-Validated'
                    event_dict = ticket_dict.get('event')

                    event_name = event_dict.get('name')
                    event_time = event_dict.get('time')
                    auditorium_dict = event_dict.get('auditorium')

                    auditorium_name = auditorium_dict.get('name')
                    auditorium_address = auditorium_dict.get('address')

                    auditorium = Auditorium(name=auditorium_name, address=auditorium_address)
                    for audi_in_db in auditoriums:
                        if audi_in_db.name == auditorium_name and audi_in_db.address == auditorium_address:
                            audi_do_not_exist = False
                            auditorium = audi_in_db
                            break
                    if audi_do_not_exist:
                        auditorium.save()

                    event = Event(name=event_name, time=event_time, auditorium=auditorium)
                    for event_in_db in events:
                        if event_in_db.name == event_name:
                            event_do_not_exist = False
                            event = event_in_db
                            break
                    if event_do_not_exist:
                        event.save()

                    ticket = Ticket(ticketHash=ticketHash, status=ticket_status,
                                    owner=owner, event=event)
                    for tick in tickets:
                        if tick.ticketHash == ticketHash:
                            ticket = tick
                    ticket.save()
            else:
                print('Received: No event found retry in 1 sec')
                time.sleep(1)
        except requests.exceptions.Timeout:
            print('TIMEOUT OBTAIN TICKET LIST')
        except ValueError:
            print('INVALID JSON FORMAT')
            print(response.text)

    def sendIPtoGestionWebsite(self, ipAddress):
        url = self.heroku_url+'terminals/'
        payload = {'address': ipAddress}
        try:
            print('POST: '+url+' | Payload: '+str(payload))
            response = requests.post(url, headers=self.headers, timeout=2, data=payload)
            f = open('log/POST_IP_TO_GESTION.log', 'w')
            f.write('POST: '+url+' | Payload: '+str(payload))
            f.write('\nResponse: \n')
            f.write(response.text)
            f.close()
            return True
        except requests.exceptions.Timeout:
            print('TIMEOUT: POST IP ADDRESS')
            return False

    def sendValidationStats(self, ip):
        url = self.heroku_url+'report/'
        headers = self.headers
        headers['ipAddress'] = ip
        headers['Content-Type'] = 'application/json'
        logsValidation = MobileCommLog.objects.all()
        serializer = ValidationLogSerializer(logsValidation, many=True)
        payload = json.dumps(serializer.data)
        try:
            response = requests.post(url, headers=headers, timeout=2, data=payload)
            f = open('log/POST_LOG.log', 'w')
            f.write('POST: '+url+' | Headers: '+str(headers))
            f.write('\nPayload: '+str(payload))
            f.write('\nResponse: \n')
            f.write(response.text)
            f.close()
        except requests.exceptions.Timeout:
            print('TIMEOUT: POST LOG')

    def verifyEventIsClose(self, ip):
        url = self.heroku_url+'close/'
        headers = self.headers
        headers['ipAddress'] = ip
        try:
            response = requests.get(url, headers=self.headers, timeout=2)
            print('GET: '+url+' | Headers: '+str(headers))
            f = open('log/GET_IS_CLOSE.log', 'w')
            f.write('POST: '+url+' | Headers: '+str(headers))
            f.write('\nResponse: \n')
            f.write(response.text)
            f.close()
            if 'true' in response.text:
                return True
        except requests.exceptions.Timeout:
            print('TIMEOUT: GET EVENT IS CLOSE')
        return False

    def sendIPtoPI(self, pi_ip, my_ip):
        url = 'http://'+pi_ip+':8000/api/terminal/'
        payload = {'ipAddress': my_ip, 'status': 'Connected'}
        try:
            response = requests.post(url, headers=self.headers, data=payload, timeout=2)
            print('POST: '+url+' | Payload: '+str(payload))
            f = open('log/POST_IP_TO_PI.log', 'w')
            f.write('POST: '+url+' | Payload: '+str(payload))
            f.write('\nResponse: \n')
            f.write(response.text)
            f.close()
            return False
        except requests.exceptions.Timeout:
            print('TIMEOUT: POST IP TO PI')
            return True

    def run(self):
        time.sleep(3) #To let te server start before sending a request to it
        # Write the mobile API KEY to the DB
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM rest_framework_api_key_apikey")
            cursor.execute("INSERT INTO rest_framework_api_key_apikey VALUES('1','','','mobile','ooXein0ZieZohfoh0phuCee0eeng6aomu6tei7le9eiHo4Fai0')")
            cursor.execute("INSERT INTO rest_framework_api_key_apikey VALUES('2','','','pi','a677abfcc88c8126deedd719202e50922')")
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

        Terminal.objects.all().delete()
        Ticket.objects.all().delete()
        Event.objects.all().delete()
        Auditorium.objects.all().delete()
        # Post to Gestion website our ip address
        while not self.sendIPtoGestionWebsite(ip):
           pass
        # Query Gestion website for the terminal list
        while not self.obtainTerminalsFromGestionWebsite(ip):
           pass

        # IF no terminal in DB Query Gestion website for ticketsList
        tickets = Ticket.objects.raw('SELECT * FROM api_ticket')
        terminals = Terminal.objects.raw('SELECT * FROM api_terminal WHERE "status"="Connected"')

        for terminal in terminals:
            while self.sendIPtoPI(my_ip=ip, pi_ip=terminal.ipAddress):
                pass
        isMaster = False
        while len(list(tickets))==0:
            if len(list(terminals)) == 0 or isMaster:
                isMaster = True
                self.obtainTicketsFromGestionWebsite(ip)
            # Else Query first PI in the list for the tickets
            else:
                self.obtainTicketList(ipAddress=terminals[0].ipAddress)
            tickets = Ticket.objects.raw('SELECT * FROM api_ticket')


        while True:
            if self.verifyEventIsClose(ip):
                print('======================================== Event is close ========================================')
                print('Send log')
                self.sendValidationStats(ip)
                print('Done\nBack up DB')
                copyfile('gti525/db.sqlite3', 'gti525/db.backup.'+datetime.now().strftime('%Y-%m-%d_%H:%M:%S')+'.sqlite3')
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM api_mobilecommlog")
                print('Done')
                break
            else:
                print('Not close')
                time.sleep(10)

    def launch(self):
        self.run()
