from django.http import HttpResponse
from django.http import Http404
import mapscript

from giosystemcore.tools.ows import Mapfile

import models
import ows

def wms_endpoint(request, mapfile=None):
    '''
    WMS endpoint.
    '''

    if mapfile is None:
        try:
            m = models.MapObj.objects.all()[0]
        except IndexError:
            raise Http404
    else:
        try:
            m = models.MapObj.objects.get(name=mapfile)
        except models.MapObj.DoesNotExist:
            raise Http404
    map_obj = m.build_mapfile()
    result, ct = ows.process_request(request, map_obj)
    content_type = ows.get_content_type(ct)
    response = HttpResponse(content_type=content_type)
    response.write(result)
    return response


