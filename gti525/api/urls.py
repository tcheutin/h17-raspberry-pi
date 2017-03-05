from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/tickets/$', views.TicketList.as_view()),
    url(r'^api/ticket/validate/(?P<ticketHash>\w+)/$', views.TicketValidation.as_view()),
    url(r'^api/terminals/$', views.TerminalList.as_view())
]
