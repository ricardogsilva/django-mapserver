from django.http import HttpResponse
import mapscript

from giosystemcore.tools.ows import Mapfile

def wms_endpoint(request):
    '''
    WMS endpoint.
    '''

    if request.method == 'GET':
        params = request.GET
    elif request.method == 'POST':
        # get the params from the XML body of the request
        raise Exception

    # get or build our mapfile
    map_obj = get_mapfile(request)

    # send the request to mapserver
    ms_output = process_wms_request(params, map_obj)

    # create django's response, setting appropriate headers and content-type
    response = HttpResponse()
    response.write(ms_output)

    return response

def process_wms_request(request, mapfile):
    '''
    Offload the processing of the WMS request to MapServer.

    :arg request: the request parameters
    :type request: dict
    :arg mapfile: the in-memory mapfile to use
    :type mapfile: mapscript.mapObj

    :return: the mapserver buffer with the output from processing the request
    '''

    # build the WMS request
    wms_req = mapscript.OWSRequest()
    for k, v in request.iteritems():
        wms_req.setParameter(k, v)

    # install a mapserver IO handler directing future stdout to a memory buffer
    output_buffer = mapscript.msIO_installStdoutToBuffer()

    # dispatch the request to mapserver
    mapfile.OWSDispatch(wms_req)

    # get back mapserver's response
    # ms_headers = mapscript.msIO_stripStdoutBufferContentHeaders()
    # ms_content_type = mapscript.msIO_stripStdoutBufferContentType()
    ms_content = mapscript.msIO_getStdoutBufferByes()

    # reset the stdin/stdout handlers
    msIO_resetHandlers()

    return ms_content

def get_mapfile(request):
    '''
    Get or create a new mapfile.

    Re-implement this in your custom code.
    '''

    name = ''
    shape_path = ''
    host = ''
    extent = (0, 0, 0, 0)
    background_color = (255, 255, 255)
    layers = []
    m = Mapfile(name, shape_path, host, extent, background_color, layers)
    map_obj = m.create_mapfile()
    return map_obj
