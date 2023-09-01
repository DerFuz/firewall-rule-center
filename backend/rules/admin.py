from django.contrib import admin

from .models import Rule, FirewallObject

admin.site.register(Rule)
admin.site.register(FirewallObject)

