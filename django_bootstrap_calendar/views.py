# -*- coding: utf-8 -*-
__author__ = 'sandlbn and w3lly'

from django.views.generic import ListView, TemplateView
from models import CalendarEvent
from serializers import event_serializer
from utils import timestamp_to_datetime
from django.http import HttpResponse,HttpResponseRedirect

import datetime

class CalendarJsonListView(ListView):

    template_name = 'django_bootstrap_calendar/calendar_events.html'
	
    def get_queryset(self):
        queryset = CalendarEvent.objects.filter()
        from_date = self.request.GET.get('from', False)
        to_date = self.request.GET.get('to', False)
        #user = self.request.GET.get('')
        if from_date and to_date:
            queryset = queryset.filter(
                start__range=(
                    timestamp_to_datetime(from_date) + datetime.timedelta(-30),
                    timestamp_to_datetime(to_date)
                    )
            )
        elif from_date:
            queryset = queryset.filter(
                start__gte=timestamp_to_datetime(from_date)
            )
        elif to_date:
            queryset = queryset.filter(
                end__lte=timestamp_to_datetime(to_date)
            )

        return event_serializer(queryset)



class CalendarView(TemplateView):
			template_name = 'django_bootstrap_calendar/calendar.html'
	
	
# def add_event_view(request):
# var	calendar = $('#calendar').calendar({
# events_source: [
	# {
		# "id": 293,
		# "title": "Event 1",
		# "url": "http://example.com",
		# "class": "event-important",
		# "start": 12039485678000, // Milliseconds
		# "end": 1234576967000 // Milliseconds
	# },
# ]});
	# return render(request,'django_bootstrap_calendar/calendar_events.html')
	# return HttpResponseRedirect("")
	

	
