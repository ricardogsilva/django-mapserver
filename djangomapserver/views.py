from django.http import HttpResponse
import mapscript

from giosystemcore.tools.ows import Mapfile

import models
import ows

def wms_endpoint(request, mapfile=None):
    '''
    WMS endpoint.
    '''

    if mapfile is None:
        m = models.MapFile.objects.all()[0]
    else:
        m = models.MapFile.objects.get(name=mapfile)
    layer_names = request.GET('layers')
    map_obj = ows.create_mapfile(m, layer_names)
    result, ct = ows.process_request(request, map_obj)
    content_type = ows.get_content_type(ct)
    response = HttpResponse(content_type=content_type)
    response.write(result)
    return response


