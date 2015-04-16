from django.contrib import admin

import models

class SpatialiteDataStoreAdmin(admin.ModelAdmin):
    pass


class ShapefileDataStoreAdmin(admin.ModelAdmin):
    pass


class PostGisDataStoreAdmin(admin.ModelAdmin):
    pass


class RasterDataStoreAdmin(admin.ModelAdmin):
    pass


class RectObjAdmin(admin.ModelAdmin):
    pass

class MapServerColorAdmin(admin.ModelAdmin):
    pass

class MapLayerInline(admin.StackedInline):
    model = models.MapLayer
    extra = 1

class MapObjAdmin(admin.ModelAdmin):
    inlines = [MapLayerInline]
    list_display = ("name", "projection", "available_layers")

class StyleObjInline(admin.StackedInline):
    model = models.StyleObj

class ClassObjAdmin(admin.ModelAdmin):
    inlines = [StyleObjInline]
    list_display = ("name", "layer_obj",)

class LayerObjAdmin(admin.ModelAdmin):
    list_display = ("name", "projection", "extent", "layer_type",
                    "data_store")

admin.site.register(models.RectObj, RectObjAdmin)
admin.site.register(models.MapServerColor, MapServerColorAdmin)
admin.site.register(models.MapObj, MapObjAdmin)
admin.site.register(models.LayerObj, LayerObjAdmin)
admin.site.register(models.ClassObj, ClassObjAdmin)
admin.site.register(models.ShapefileDataStore, ShapefileDataStoreAdmin)
admin.site.register(models.SpatialiteDataStore, SpatialiteDataStoreAdmin)
admin.site.register(models.PostgisDataStore, PostGisDataStoreAdmin)
admin.site.register(models.RasterDataStore, RasterDataStoreAdmin)
