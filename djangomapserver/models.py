"""
Django models that align with MapServer"s mapscript API
"""

from django.db import models
import mapscript

class MapObj(models.Model):
    STATUS_CHOICES = (
        (mapscript.MS_OFF, "off"),
        (mapscript.MS_ON, "on"),
        (mapscript.MS_DEFAULT, "default")
    )
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
    shape_path = models.CharField(max_length=255, help_text="Base filesystem "
                                  "path to layer data.")
    cell_size = models.FloatField(help_text="Pixel size in map units.",
                                  blank=True, null=True)
    extent = models.ForeignKey("RectObj", help_text="Map's spatial extent.")
    # font_set
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES)
    image_color = models.ForeignKey("MapServerColor",
                                    help_text="Initial map background color.",
                                    null=True, blank=True)
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
        return m


class LayerObj(models.Model):
    name = models.CharField(max_length=255)
    map_obj = models.ForeignKey('MapObj')
    class_item = models.CharField(
        max_length=255, 
        help_text="Item name in attribute table to use for class lookups."
    )
    data = models.CharField(max_length=255, help_text="Full filename of the "
                            "spatial data to process.")
    ows_abstract = models.TextField(blank=True)
    ows_enable_request = models.CharField(max_length=255, default="*")
    ows_extent = models.ForeignKey("RectObj", help_text="Layer's spatial extent.")
    ows_include_items = models.CharField(max_length=50, default="all",
                                         blank=True)
    gml_include_items = models.CharField(max_length=50, default="all",
                                         blank=True)
    ows_opaque = models.SmallIntegerField(blank=True, null=True)
    # ows_srs will be the same as the corresponing map
    # ows_title is the same as the layer's name

    def __unicode__(self):
        return self.name


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

    def __unicode__(self):
        result = u"RGB({}, {}, {})".format(self.red, self.green,
                                           self.blue)
        return result

class RectObj(models.Model):
    max_x = models.FloatField()
    max_y = models.FloatField()
    min_x = models.FloatField()
    min_y = models.FloatField()

    def __unicode__(self):
        return "{}, {}, {}, {}".format(self.min_x, self.max_x, self.min_y,
                                       self.max_y)
