"""
Django models that align with MapServer"s mapscript API
"""

import os

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.contrib.gis.gdal.geometries as gdal_geometries
from django.contrib.gis.gdal import DataSource

import mapscript

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
    projection = models.CharField(
        max_length=255, default= "init=epsg:4326",
        help_text="PROJ4 definition of the map projection"
    )
    units = models.SmallIntegerField(choices=UNITS_CHOICES, blank=True)
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

    def __unicode__(self):
        return self.name

    def build_mapfile(self):
        """
        Build a mapObj
        """

        m = mapscript.mapObj()
        m.name = self.name
        m.setProjection(self.projection)
        m.shapepath = self.shape_path
        m.units = self.units
        m.setMetaData("ows_title", self.name)
        m.setMetaData("ows_onlineresource",
                      "http://{}{}".format(settings.HOST_NAME, ""))
        m.setMetaData("ows_srs", self.projection)
        m.setMetaData("ows_enable_request", "")
        m.setMetaData("ows_encoding", "utf-8")
        m.imagetype = "png"
        m.extent = self.extent.build_rect_obj()
        m.setSize(*self.MAP_SIZE)
        m.imageColor = self.image_color.build_color()
        for la in self.layers:
            m.insertLayer(la.build_layer())
        return m


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
    projection = models.CharField(
        max_length=255, default= "init=epsg:4326",
        help_text="PROJ4 definition of the layer projection"
    )
    extent = models.ForeignKey("RectObj", help_text="Layer's spatial extent.")
    data = models.CharField(max_length=255, help_text="Full filename of the "
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

    def build_layer(self):
        """
        Build a mapscript LayerObj
        """

        layer = mapscript.layerObj()
        layer.name = self.name
        layer.status = mapscript.MS_ON
        layer.template = "templates/blank.html"
        layer.dump = mapscript.MS_TRUE
        #setProjection
        layer_meta = mapscript.hashTableObj()
        layer_meta.set("ows_title", self.name)
        layer_meta.set("ows_srs", self.map_obj.projection)
        layer_meta.set("ows_include_items", "all")
        layer_meta.set("gml_include_items", "all")
        layer_meta.set("wcs_label", self.name)
        layer_meta.set("wcs_rangeset_name", "range 1")
        layer_meta.set("wcs_rangeset_label", "my label")
        layer.metadata = layer_meta
        layer.data = self.data
        layer.type = self.layer_type
        return layer


    def __unicode__(self):
        return self.name


class MapLayer(models.Model):
    map_obj = models.ForeignKey(MapObj)
    layer_obj = models.ForeignKey(LayerObj)
    status = models.SmallIntegerField(choices=STATUS_CHOICES)
    style = models.ForeignKey("StyleObj", null=True, blank=True)

class DataStoreBase(models.Model):

    def __unicode__(self):
        try:
            result = self.spatialitedatastore
        except self.DoesNotExist:
            result = self.shapefiledatastore
        return result


class SpatialiteDataStore(DataStoreBase):
    path = models.CharField(max_length=255, help_text="Path to the Spatialite "
                            "database file.")

    def __unicode__(self):
        return "spatialite:{}".format(self.path)


class ShapefileDataStore(DataStoreBase):
    path = models.CharField(max_length=255, help_text="Path to the directory "
                            "holding shapefiles.")

    def __unicode__(self):
        return "shapefile:{}".format(self.path)


class ClassObj(models.Model):
    layer_obj = models.ForeignKey("LayerObj")
    expression = models.CharField(max_length=255)

    def __unicode__(self):
        return self.expression


class StyleObj(models.Model):
    class_obj = models.ForeignKey("ClassObj")
    color = models.ForeignKey("MapServerColor")


class MapServerColor(models.Model):
    red = models.IntegerField(blank=True, null=True)
    green = models.IntegerField(blank=True, null=True)
    blue = models.IntegerField(blank=True, null=True)
    hex_string = models.CharField(max_length=9, blank=True)
    attribute = models.CharField(max_length=255, blank=True)

    def build_color(self):
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

    def build_rect_obj(self):
        return mapscript.rectObj(self.min_x, self.min_y, 
                                 self.max_x, self.max_y)

    def __unicode__(self):
        return "{}, {}, {}, {}".format(self.min_x, self.max_x, self.min_y,
                                       self.max_y)

def _get_mapserver_geometry(ogr_geometry):
    geom_map = {
        mapscript.MS_LAYER_POINT: [],
        mapscript.MS_LAYER_LINE: ['LineString',],
        mapscript.MS_LAYER_POLYGON: [],
    }
    result = None
    for ms_geom, ogr_geoms in geom_map.iteritems():
        if ogr_geometry in ogr_geoms:
            result = ms_geom
    return result

# signals


# FIXME - Check if the layers are already present in the database before adding
# FIXME - Check if the extent has already been defined and reuse it
@receiver(post_save, sender=ShapefileDataStore)
def find_shapefile_layers(sender, **kwargs):
    """
    Scan the path value of the newly created ShapefileDataStore and new layers
    """

    for dirpath, dirnames, fnames in os.walk(kwargs['instance'].path):
        for file_ in (f for f in fnames if 
                os.path.splitext(f) == SHAPEFILE_EXTENSION):
            file_path = os.path.join(dirpath, file_)
            ds = DataSource(file_path)
            ds_layer = ds[0]  # shapefiles only have one layer
            layer = LayerObj(
                name = ds_layer.name,
                layer_type= _get_mapserver_geometry(ds_layer.geom_type.name),
                data_store=kwargs['instance'].pk,
                projection=ds_layer.srs.proj4,
                data=file_path,
                extent=RectObj(
                    min_x=ds_layer.extent.min_x,
                    min_y=ds_layer.extent.min_y,
                    max_x=ds_layer.extent.max_x,
                    max_y=ds_layer.extent.max_y
                )
            )
            layer.save()
