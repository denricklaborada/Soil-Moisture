from django.contrib import admin
from .models import *

class NodeAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)


admin.site.register(Node, NodeAdmin)
