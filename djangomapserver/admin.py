from django.contrib import admin

import models

class RectObjAdmin(admin.ModelAdmin):
    pass

class MapServerColorAdmin(admin.ModelAdmin):
    pass

class LayerObjInline(admin.StackedInline):
    model = models.LayerObj
    extra = 1

class MapObjAdmin(admin.ModelAdmin):
    inlines = [LayerObjInline]

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
