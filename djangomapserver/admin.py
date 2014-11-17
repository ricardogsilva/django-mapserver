from django.contrib import admin

import models

class SpatialiteDataStoreAdmin(admin.ModelAdmin):
    pass


class ShapefileDataStoreAdmin(admin.ModelAdmin):
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

class StyleObjInline(admin.StackedInline):
    model = models.StyleObj

class ClassObjAdmin(admin.ModelAdmin):
    inlines = [StyleObjInline]

class ClassObjInline(admin.StackedInline):
    model = models.ClassObj

class LayerObjAdmin(admin.ModelAdmin):
    inlines = [ClassObjInline]

admin.site.register(models.RectObj, RectObjAdmin)
admin.site.register(models.MapServerColor, MapServerColorAdmin)
admin.site.register(models.MapObj, MapObjAdmin)
admin.site.register(models.LayerObj, LayerObjAdmin)
admin.site.register(models.ClassObj, ClassObjAdmin)
admin.site.register(models.ShapefileDataStore, ShapefileDataStoreAdmin)
admin.site.register(models.SpatialiteDataStore, SpatialiteDataStoreAdmin)
