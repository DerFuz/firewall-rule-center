from django.contrib import admin

from .models import Rule, RuleAction, RuleProtocol, RuleStatus, FirewallObject

admin.site.register(Rule)
admin.site.register(RuleAction)
admin.site.register(RuleProtocol)
admin.site.register(RuleStatus)
admin.site.register(FirewallObject)

