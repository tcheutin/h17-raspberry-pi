from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/tickets/$', views.TicketList.as_view()),
    url(r'^api/ticket/validate/(?P<ticketHash>[0-9a-f-]+)/$', views.TicketValidation.as_view()),
    url(r'^api/ticket/(?P<ticketHash>[0-9a-f-]+)/$', views.TicketValidation.as_view()),
    url(r'^api/terminals/$', views.TerminalList.as_view()),
    url(r'^api/terminal/$', views.TerminalList.as_view())
]
