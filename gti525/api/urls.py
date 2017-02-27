from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^api/tickets/$', views.TicketList.as_view()),
    url(r'^api/ticket/(?P<ticketHash>\w+)/$', views.TicketDetail.as_view()),
    url(r'^api/terminals/$', views.TerminalList.as_view())
]
