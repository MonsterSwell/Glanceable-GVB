from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render_to_response

import logging
import urllib2
import datetime
import time
import json

from xml.dom.minidom import parseString

logger = logging.getLogger(__name__)


from govi.stops import HALTES
HALTES = sorted(HALTES, key=lambda halte: halte['name'])


def index(request):
    halteids = request.GET.get('halteids', '').split(',')
    
    return render_to_response('govi/index.html', {
        'halteids': halteids
    }, context_instance=RequestContext(request))
    
def pick(request):
    return render_to_response('govi/pick.html', {
        'haltes': HALTES,
        'haltesjson': json.dumps(HALTES)
    }, context_instance=RequestContext(request))
    
def haltes(request):
    return HttpResponse(json.dumps(HALTES), mimetype="application/json")
    
def halte(request, halteid):
    return HttpResponse(json.dumps([halte for halte in HALTES if halte['id']==halteid][0]), mimetype="application/json")
    
def dris(request, halteid):
    dris = urllib2.urlopen('http://cache.govi.openov.nl/kv55/%s' % halteid).read()
    dom = parseString(dris)
    
    trips = dom.getElementsByTagName('Trip')
    
    now = datetime.datetime.now()
    
    destination = ''
    minutesUntil = []
    
    for trip in trips:
        destination = trip.getElementsByTagName('DestinationName')[0].childNodes[0].data
        expected = trip.getElementsByTagName('ExpectedDepartureTime')[0].childNodes[0].data
        
        expectedTime = datetime.datetime(now.year, now.month, now.day, int(expected.split(':')[0]), int(expected.split(':')[1]), int(expected.split(':')[2]))
        
        minutesUntil.append((expectedTime - now).seconds / 60)
        
    return HttpResponse(json.dumps({'destination': destination, 'minutes': minutesUntil}), mimetype='application/json')