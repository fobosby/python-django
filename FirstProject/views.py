import datetime
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template

__author__ = 'alexey'
from django.http import HttpResponse, Http404


def hello(request):
    return HttpResponse("Hello World - This is response!")


def current_time(request):
    #result = "Current time is %s." % datetime.datetime.now()
    #return HttpResponse(result)
    return render_to_response('CurrentTime.html', {'current_time': datetime.datetime.now()})


def shifted_time(request, hour_shift, minute_shift):
    try:
        hours = int(hour_shift)
        minutes = int(minute_shift)
    except ValueError:
        raise Http404()
    time = datetime.datetime.now()+datetime.timedelta(hours=hours, minutes=minutes)
    #return HttpResponse("Shifted time is %s. Hour shift = %s, minute shift = %s" % (time, hour_shift, minute_shift))
    return render_to_response('ShiftedTime.html', locals())


def template_time(request):
    now = datetime.datetime.now()
    #template = get_template("TestTemplate.html")
    #return HttpResponse(template.render(Context({'current_date': now})))

    return render_to_response('TestTemplate.html',{'current_date': now})