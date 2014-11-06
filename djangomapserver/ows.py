'''
Some helper functions to allow Django to serve as a wrapper for MapServer.
'''

import mapscript

def process_request(django_request, map_obj):
    '''
    Offload the processing of the OWS request to MapServer.

    :arg django_request: the request parameters
    :type django_request: HttpRequest
    :arg map_obj: the in-memory mapfile to use
    :type map_obj: mapscript.mapObj

    :return: the mapserver buffer with the output from processing the request
    '''

    if django_request.method == 'GET':
        params = django_request.GET
    elif django_request.method == 'POST':
        # get the params from the XML body of the request
        raise Exception
    # build the WMS request
    wms_req = mapscript.OWSRequest()
    for k, v in params.iteritems():
        wms_req.setParameter(k, v)

    # install a mapserver IO handler directing future stdout to a memory buffer
    output_buffer = mapscript.msIO_installStdoutToBuffer()

    # dispatch the request to mapserver
    map_obj.OWSDispatch(wms_req)

    # get back mapserver's response
    # ms_headers = mapscript.msIO_stripStdoutBufferContentHeaders()
    ms_content_type = mapscript.msIO_stripStdoutBufferContentType()
    ms_content = mapscript.msIO_getStdoutBufferBytes()
    if ms_content == 'application/vnd.ogc.se_xml':
        ms_content = 'Content-Type: text/xml\n\n{}'.format(ms_content)

    # reset the stdin/stdout handlers
    mapscript.msIO_resetHandlers()

    return ms_content, ms_content_type

def get_content_type(mapserver_output_content_type):
    result = None
    if mapserver_output_content_type == 'application/vnd.ogc.se_xml':
        result = 'text/xml'
    else:
        result = mapserver_output_content_type
    return result
