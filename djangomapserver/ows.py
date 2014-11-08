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

def create_mapfile(model):
    mapfile = mapscript.mapObj()
    # mapfile.name = wms_title
    # mapfile.setProjection(projection)
    # mapfile.shapepath = '/root/of/the/bogus'
    # mapfile.units = mapscript.MS_DD
    # mapfile.setMetaData('wms_title', wms_title)
    # mapfile.setMetaData('wcs_onlineresource', 'http://{}{}'.format(
    #     settings.HOST_NAME, request_path)
    # )
    # mapfile.setMetaData('wms_srs', projection)
    # mapfile.setMetaData('wms_enable_request', '*')
    # mapfile.setMetaData('wms_encoding', 'utf-8')
    # mapfile.setMetaData('wcs_enable_request', '*')
    # mapfile.setMetaData('wcs_label', wms_title)
    # mapfile.imagetype = 'png'
    # mapfile.extent = mapscript.rectObj(-180.0, -90.0, 180.0, 90.0)
    # mapfile.setSize(800, 600)
    # mapfile.imageColor = mapscript.colorObj(255, 255, 255)
    # layers = [
    #     ('lst', '/home/ricardo/giosystem_data/OUTPUT_DATA/POST_PROCESS/geotiffs/LST/2014/09/15/g2_BIOPAR_LST_201409150900_EURO_GEO_v1_LST.tif', ''),
    # ]
    # for layer, path, palette in layers:
    #     new_layer = mapscript.layerObj()
    #     new_layer.name = layer
    #     new_layer.status = mapscript.MS_ON
    #     new_layer.template = 'templates/blank.html'
    #     new_layer.dump = mapscript.MS_TRUE
    #     new_layer.setProjection(projection)
    #     layer_meta = mapscript.hashTableObj()
    #     layer_meta.set('wms_title', layer)
    #     layer_meta.set('wms_srs', projection)
    #     layer_meta.set('wms_include_items', 'all')
    #     layer_meta.set('gml_include_items', 'all')
    #     layer_meta.set('wcs_label', layer)
    #     layer_meta.set('wcs_rangeset_name', 'range ')
    #     layer_meta.set('wcs_rangeset_label', 'my label')
    #     new_layer.metadata = layer_meta
    #     new_layer.data = path
    #     new_layer.type = mapscript.MS_LAYER_RASTER
    #     # add the pallete stuff here
    #     mapfile.insertLayer(new_layer)
    # return mapfile

