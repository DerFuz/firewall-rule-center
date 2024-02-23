from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

GROUPS = {
    "nw-admin": {
        #general permissions
        "permission" : ["view"],
        "group" : ["view"],
        "user" : ["view"],

        #django app model specific permissions
        "firewallobject" : ["add", "delete", "change", "view"],
        "historicalfirewall object" : ["view"],
        "historicalrule" : ["view"],
        "historicalrule_firewalls" : ["view"],
        "rule" : ["add", "delete", "change", "view"],
        "historicalrulesetrequest" : ["view"],
        "rulesetrequest" : ["add", "delete", "change", "view"],
    },

    "normal-user": {
        #general permissions
        "user" : ["view"],
        
        #django app model specific permissions
        "firewallobject" : ["view"],
        "historicalrule" : ["view"],
        "historicalrule_firewalls" : ["view"],
        "rule" : ["view"],
        "historicalrulesetrequest" : ["view"],
        "rulesetrequest" : ["view"],
    },
    
    "auditor": {
        #general permissions
        "user" : ["view"],
        
        #django app model specific permissions
        "firewallobject" : ["view"],
        "historicalrule" : ["view"],
        "historicalrule_firewalls" : ["view"],
        "rule" : ["add", "view"],
        "historicalrulesetrequest" : ["view"],
        "rulesetrequest" : ["add", "view"],
    },
}

class Command(BaseCommand):

    help = "Creates default permissions for DRF groups (nw-admin, normal-user, auditor)"

    def handle(self, *args, **options):
        
        for group_name in GROUPS:

            new_group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for app_model in GROUPS[group_name]:

                # Loop permissions in group/model
                for permission_name in GROUPS[group_name][app_model]:

                    # Generate permission codename as Django would generate it
                    codename = f"{permission_name}_{app_model}"

                    try:
                        model_add_perm = Permission.objects.get(codename=codename)
                        print(f"Added permission \"{codename}\" to group \"{new_group}\"")
                    except Permission.DoesNotExist:
                        print(f"Permission not found with codename '{codename}'.")
                        continue

                    new_group.permissions.add(model_add_perm)