from django.contrib import admin
from django.db.models import get_model


admin.site.register(get_model('fancypages', 'FancyPage'))
admin.site.register(get_model('fancypages', 'PageType'))
admin.site.register(get_model('fancypages', 'PageGroup'))
admin.site.register(get_model('fancypages', 'Container'))
admin.site.register(get_model('fancypages', 'OrderedContainer'))
