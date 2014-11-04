from django.http import HttpResponse
import mapscript

def wms_endpoint(request):
    '''
    WMS endpoint.
    '''

    return HttpResponse('<h1>this is the wms endpoint</h1>')
