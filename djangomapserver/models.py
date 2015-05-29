"""
Django models that align with MapServer's mapscript API
"""

# TODO - Add a geotiff datastore that is recursive, like the shapefile one

import os

from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.gdal import DataSource
from django.contrib.sites.models import Site
from osgeo import osr
import mapscript

import validators

STATUS_CHOICES = (
    (mapscript.MS_OFF, "off"),
    (mapscript.MS_ON, "on"),
    (mapscript.MS_DEFAULT, "default")
)

SHAPEFILE_EXTENSION = 'shp'

class MapObj(models.Model):
    MAP_SIZE = (800, 600)
    IMAGE_TYPE_CHOICES = (
        ("png", "png"),
    )
    UNITS_CHOICES = (
        (mapscript.MS_DD, "Decimal degrees"),
    )
    name = models.CharField(max_length=255, help_text="Unique identifier.")
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    projection = models.PositiveSmallIntegerField(
        default= 4326, help_text="EPSG code of the map projection"
    )
    units = models.SmallIntegerField(choices=UNITS_CHOICES)
    size = models.CommaSeparatedIntegerField(help_text="Map size in pixel units",
                                             max_length=10)
    cell_size = models.FloatField(help_text="Pixel size in map units.",
                                  blank=True, null=True)
    extent = models.ForeignKey("RectObj", help_text="Map's spatial extent.")
    # font_set
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES)
    image_color = models.ForeignKey("MapServerColor",
                                    help_text="Initial map background color.",
                                    null=True, blank=True)
    layers = models.ManyToManyField("LayerObj", null=True, blank=True,
                                    through="MapLayer")
    # legend
    # metadata (see what parameters refer to each service)
    # ows_title is the same as the map's name
    ows_sld_enabled = models.BooleanField(default=True)
    ows_abstract = models.TextField(blank=True)
    ows_enable_request = models.CharField(max_length=255, default="*")
    ows_encoding = models.CharField(max_length=20, default="utf-8")
    # ows_onlineresource does not need to be editable
    # ows_srs uses the same projection as the map and does not need to be editable

    def build(self):
        """
        Build a mapObj
        """

        uri = reverse("wms_endpoint")
        m = mapscript.mapObj()
        m.name = self.name
        m.setProjection("init=epsg:{}".format(self.projection))
        m.shapepath = ""
        m.units = self.units
        m.setMetaData("ows_title", self.name)
        m.setMetaData("ows_onlineresource",
                      "http://{}{}".format(Site.objects.get_current().domain, uri))
        m.setMetaData("wms_srs", "EPSG:{}".format(self.projection))
        m.setMetaData("wms_enable_request", self.ows_enable_request)
        m.setMetaData("wms_encoding", "utf-8")
        m.imagetype = "png"
        m.extent = self.extent.build()
        m.setSize(*self.MAP_SIZE)
        if self.image_color is not None:
            m.imageColor = self.image_color.build()
        else:
            m.imageColor = mapscript.colorObj(255, 255, 255)
        for layer in self.layers.all():
            m.insertLayer(layer.build())
        return m

    def _available_layers(self):
        return ', '.join((la.name for la in self.layers.all()))
    available_layers = property(_available_layers)

    def __unicode__(self):
        return self.name


class LayerObj(models.Model):
    LAYER_TYPE_CHOICES = (
        (mapscript.MS_LAYER_RASTER, "raster"),
        (mapscript.MS_LAYER_POLYGON, "vector polygon"),
        (mapscript.MS_LAYER_LINE, "vector line"),
        (mapscript.MS_LAYER_POINT, "vector point"),
    )
    name = models.CharField(max_length=255)
    layer_type = models.SmallIntegerField(choices=LAYER_TYPE_CHOICES)
    data_store = models.ForeignKey("DataStoreBase")
    projection = models.PositiveSmallIntegerField(
        default= 4326, help_text="EPSG code of the layer projection"
    )
    extent = models.ForeignKey("RectObj", help_text="Layer's spatial extent.")
    data = models.CharField(max_length=255, help_text="Full path to the "
                            "spatial data to process.")
    class_item = models.CharField(
        max_length=255,
        help_text="Item name in attribute table to use for class lookups.",
        blank=True
    )
    ows_abstract = models.TextField(blank=True)
    ows_enable_request = models.CharField(max_length=255, default="*")
    ows_include_items = models.CharField(max_length=50, default="all",
                                         blank=True)
    gml_include_items = models.CharField(max_length=50, default="all",
                                         blank=True)
    ows_opaque = models.SmallIntegerField(blank=True, null=True)
    # ows_srs will be the same as the corresponing map
    # ows_title is the same as the layer's name

    def build(self):
        """
        Build a mapscript LayerObj
        """

        layer = mapscript.layerObj()
        layer.name = self.name
        layer.status = mapscript.MS_ON
        layer.template = "templates/blank.html"
        layer.dump = mapscript.MS_TRUE
        layer.setProjection("init=epsg:{}".format(self.projection))
        layer.metadata.set("wms_title", self.name)
        layer.metadata.set("wms_srs", "EPSG:{}".format(self.projection))
        layer.metadata.set("wms_include_items", "all")
        layer.metadata.set("gml_include_items", "all")
        #layer.metadata.set("wcs_label", self.name)
        #layer.metadata.set("wcs_rangeset_name", "range 1")
        #layer.metadata.set("wcs_rangeset_label", "my label")
        layer.type = self.layer_type
        #layer.connectiontype = self.data_store.connection_type
        #layer.connection = self.data
        layer.data = self.data
        for c in self.classobj_set.all():
            layer.insertClass(c.build())
        # Connection stuff for PostGIS
        if self.data_store.connection_type == mapscript.MS_POSTGIS:
            test_dict = {
                'host': 'localhost',
                'database': 'mapserver',
                'user': 'mapserver',
                'password': 'mapserver',
                'port': 5432
            }
            layer.connectiontype = mapscript.MS_POSTGIS
            layer.connection = "host={host} dbname={database} user={user} password={password} port={port}".format(**test_dict)
        return layer

    def __unicode__(self):
        return self.name


class MapLayer(models.Model):
    map_obj = models.ForeignKey(MapObj)
    layer_obj = models.ForeignKey(LayerObj)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.layer_obj.name


class DataStoreBase(models.Model):

    @property
    def connection_type(self):
        if hasattr(self, "rasterdatastore"):
            ct = self.rasterdatastore.connection_type
        elif hasattr(self, "shapefiledatastore"):
            ct = self.shapefiledatastore.connection_type
        elif hasattr(self, "spatialitedatastore"):
            ct = self.spatialitedatastore.connection_type
        elif hasattr(self, "postgisdatastore"):
            ct = self.postgisdatastore.connection_type
        return ct

    def __unicode__(self):
        if hasattr(self, "rasterdatastore"):
            ds = self.rasterdatastore
        elif hasattr(self, "shapefiledatastore"):
            ds = self.shapefiledatastore
        elif hasattr(self, "spatialitedatastore"):
            ds = self.spatialitedatastore
        elif hasattr(self, "postgisdatastore"):
            ds = self.postgisdatastore
        return ds.__unicode__()


class SpatialiteDataStore(DataStoreBase):
    path = models.CharField(max_length=255, help_text="Path to the Spatialite "
                            "database file.")
    connection_type = mapscript.MS_OGR

    def __unicode__(self):
        return "spatialite:{}".format(self.path)

    class Meta:
        verbose_name = "Spatialite Datastore"


class ShapefileDataStore(DataStoreBase):
    path = models.CharField(max_length=255, help_text="Path to the directory "
                            "holding shapefiles.")
    connection_type = mapscript.MS_SHAPEFILE

    def __unicode__(self):
        return "shapefile:{}".format(self.path)

    class Meta:
        verbose_name = "Shapefile Datastore"


class PostgisDataStore(DataStoreBase):
    database = models.CharField(max_length=255, blank=False, help_text="Database name.")
    user = models.CharField(max_length=255, blank=False, help_text="Database user name.")
    password = models.CharField(max_length=255, blank=False, help_text="Database user password.")
    host = models.CharField(max_length=255, blank=False, default="localhost", help_text="Database host address.")
    port = models.IntegerField(default=5432, blank=False, help_text="Database host listening port.")
    connection_type = mapscript.MS_POSTGIS

    def __unicode__(self):
        return "postgis:{user}:{password}@{host}:{port}/{database}".format(**self.__dict__)

    class Meta:
        verbose_name = "PostGIS Datastore"


class RasterDataStore(DataStoreBase):
    path = models.CharField(max_length=255, help_text="Path to the directory "
                            "holding raster files.")
    connection_type = None  # rasters cannot have this attribute

    def __unicode__(self):
        return "raster:{}".format(self.path)

    class Meta:
        verbose_name = "Raster Datastore"


class ClassObj(models.Model):
    name = models.CharField(max_length=50)
    layer_obj = models.ForeignKey("LayerObj")
    expression = models.CharField(max_length=255, blank=True)

    def build(self):
        cl = mapscript.classObj()
        cl.name = self.name
        cl.setExpression(self.expression)
        for style in self.styleobj_set.all():
            cl.insertStyle(style.build())
        return cl

    def __unicode__(self):
        return self.name


class StyleObj(models.Model):
    class_obj = models.ForeignKey("ClassObj")
    color = models.ForeignKey("MapServerColor")

    def build(self):
        st = mapscript.styleObj()
        st.color = self.color.build()
        # can add more things to style in the future
        return st


class MapServerColor(models.Model):
    red = models.IntegerField(blank=True, null=True, validators=[validators.validate_integer_color])
    green = models.IntegerField(blank=True, null=True, validators=[validators.validate_integer_color])
    blue = models.IntegerField(blank=True, null=True, validators=[validators.validate_integer_color])
    hex_string = models.CharField(max_length=9, blank=True, validators=[validators.validate_hex_color])
    attribute = models.CharField(max_length=255, blank=True)

    def build(self):
        return mapscript.colorObj(self.red, self.green, self.blue)

    def __unicode__(self):
        result = u"RGB({}, {}, {})".format(self.red, self.green,
                                           self.blue)
        return result


class RectObj(models.Model):
    max_x = models.FloatField()
    max_y = models.FloatField()
    min_x = models.FloatField()
    min_y = models.FloatField()

    def build(self):
        return mapscript.rectObj(self.min_x, self.min_y,
                                 self.max_x, self.max_y)

    def __unicode__(self):
        return "{}, {}, {}, {}".format(self.min_x, self.max_x, self.min_y,
                                       self.max_y)

def _get_mapserver_geometry(ogr_geometry):
    geom_map = {
        mapscript.MS_LAYER_POINT: [],
        mapscript.MS_LAYER_LINE: ["MultiLineString", "LineString",],
        mapscript.MS_LAYER_POLYGON: ["Polygon", "MultiPolygon"],
    }
    result = None
    for ms_geom, ogr_geoms in geom_map.iteritems():
        if ogr_geometry in ogr_geoms:
            result = ms_geom
    return result

# signals
@receiver(post_save, sender=ShapefileDataStore)
def find_shapefile_layers(sender, **kwargs):
    """
    Scan the path value of the newly created ShapefileDataStore and new layers
    """

    instance = kwargs['instance']
    for dirpath, dirnames, fnames in os.walk(instance.path):
        print("Analyzing {}".format(dirpath))
        for file_ in (f for f in fnames if
                os.path.splitext(f)[-1][1:] == SHAPEFILE_EXTENSION):
            print("found {}".format(file_))
            file_path = os.path.join(dirpath, file_)
            ds = DataSource(file_path)
            ds_layer = ds[0]  # shapefiles only have one layer
            layer = get_layer(ds_layer, instance)
            layer.save()

@receiver(post_save, sender=SpatialiteDataStore)
def find_spatialite_layers(sender, **kwargs):
    ds = DataSource(kwargs["instance"].path)
    for ds_layer in ds:
        layer = get_layer(ds_layer, kwargs["instance"])
        layer.save()

def get_layer(ds_layer, data_store):
    """
    Get a models.LayerObj from the data in the input ds_layer

    :param ds_layer:
    :return:
    """
    extent, created = RectObj.objects.get_or_create(
        min_x=ds_layer.extent.min_x,
        min_y=ds_layer.extent.min_y,
        max_x=ds_layer.extent.max_x,
        max_y=ds_layer.extent.max_y
    )
    epsg_code = get_epsg_code(ds_layer)
    layer, created = LayerObj.objects.get_or_create(
        name = ds_layer.name,
        layer_type= _get_mapserver_geometry(ds_layer.geom_type.name),
        data_store=data_store,
        projection=epsg_code,
        data=data_store.path,
        extent=extent
    )
    return layer

def get_epsg_code(dataset):
    """

    :return:
    """

    srs = osr.SpatialReference()
    srs.ImportFromWkt(dataset.srs.wkt)
    srs.AutoIdentifyEPSG()
    top_level_elements = ("GEOGCS", "PROJCS")
    code = None
    index = 0
    while code is None and index < len(top_level_elements):
        code = srs.GetAuthorityCode(top_level_elements[index])
    return int(code)

