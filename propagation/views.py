# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from .models import DNS as nameservers
import dnscache as TrackMyDNS


def propagation_index(request):
    """
    Render the index page
    """
    return render(request, 'index.html')


def trace_dns(request, country_id, record_type, domain):
    """
    Query the Nameservers around the world to check the status of the
    users DNS records
    """
    if country_id and record_type and domain:
        try:
            countryId = int(country_id) + 1
        except Exception:
            pass

        try:
            # Get the quickest nameserver for a specific country
            nameserver = nameservers.objects.filter(country=countryId).filter(available=True).order_by('responsetime')[0].ip
        except Exception:
            return HttpResponseBadRequest("No nameservers available")

        DNS = TrackMyDNS.TrackMyDNS('172.16.105.141')

        return HttpResponse("%s" % (DNS.query(str(domain.lower()), str(record_type.upper()), str(nameserver),
                                              fmt="json")), content_type="application/json")
    else:
        return HttpResponseBadRequest("Incorrect arguments")
