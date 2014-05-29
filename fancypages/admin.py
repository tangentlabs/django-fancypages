from django.contrib import admin
from django.db.models import get_model


class FancyPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'uuid')

    def name(self, obj):
        return obj.node.name

    def slug(self, obj):
        return obj.node.slug


admin.site.register(get_model('fancypages', 'FancyPage'), FancyPageAdmin)
admin.site.register(get_model('fancypages', 'PageType'))
admin.site.register(get_model('fancypages', 'PageGroup'))
admin.site.register(get_model('fancypages', 'Container'))
admin.site.register(get_model('fancypages', 'OrderedContainer'))
