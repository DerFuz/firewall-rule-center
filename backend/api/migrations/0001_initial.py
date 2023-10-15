# Generated by Django 4.2.6 on 2023-10-14 23:43

from django.db import migrations


class Migration(migrations.Migration):
       
    dependencies = [
        ('contenttypes', '__latest__'),
        ('rules', '0001_initial'),
    ]
    
    def create_groups(apps, schema_migration):
        Group = apps.get_model('auth', 'Group')
        Permission = apps.get_model('auth', 'Permission')
             
        view_permission = Permission.objects.get(codename='view_permission')
        view_group = Permission.objects.get(codename='view_group')
        view_user = Permission.objects.get(codename='view_user')
        view_historicalfirewallobject = Permission.objects.get(codename='view_historicalfirewallobject')
        add_firewallobject = Permission.objects.get(codename='add_firewallobject')
        change_firewallobject = Permission.objects.get(codename='change_firewallobject')
        delete_firewallobject = Permission.objects.get(codename='delete_firewallobject')
        view_firewallobject = Permission.objects.get(codename='view_firewallobject')
        view_historicalrule = Permission.objects.get(codename='view_historicalrule')
        view_historicalrule_firewalls = Permission.objects.get(codename='view_historicalrule_firewalls')
        add_rule = Permission.objects.get(codename='add_rule')
        change_rule = Permission.objects.get(codename='change_rule')
        delete_rule = Permission.objects.get(codename='delete_rule')
        view_rule = Permission.objects.get(codename='view_rule')
        view_historicalrulesetrequest = Permission.objects.get(codename='view_historicalrulesetrequest')
        add_rulesetrequest = Permission.objects.get(codename='add_rulesetrequest')
        change_rulesetrequest = Permission.objects.get(codename='change_rulesetrequest')
        delete_rulesetrequest = Permission.objects.get(codename='delete_rulesetrequest')
        view_rulesetrequest = Permission.objects.get(codename='view_rulesetrequest')
       
        nwadmin_permission = [
            view_permission,
            view_group,
            view_user,
            view_historicalfirewallobject,
            add_firewallobject,
            change_firewallobject,
            delete_firewallobject,
            view_firewallobject,
            view_historicalrule,
            view_historicalrule_firewalls,
            add_rule,
            change_rule,
            delete_rule,
            view_rule,
            view_historicalrulesetrequest,
            add_rulesetrequest,
            change_rulesetrequest,
            delete_rulesetrequest,
            view_rulesetrequest
        ]
        
        auditor_permission = [
            view_firewallobject,
            view_historicalrule,
            view_historicalrule_firewalls,
            view_rule,
            view_historicalrulesetrequest,
            view_rulesetrequest
        ]
        
        normaluser_permission = [
            view_firewallobject,
            view_historicalrule,
            view_historicalrule_firewalls,
            add_rule,
            view_rule,
            view_historicalrulesetrequest,
            add_rulesetrequest,
            view_rulesetrequest
        ]

        nwadmin_group = Group(name='nw-admin')
        nwadmin_group.save()
        nwadmin_group.permissions.set(nwadmin_permission)
        
        auditor_group = Group(name='auditor')
        auditor_group.save()
        auditor_group.permissions.set(auditor_permission)
        
        normaluser_group = Group(name='normal-user')
        normaluser_group.save()
        normaluser_group.permissions.set(normaluser_permission)

    operations = [
        migrations.RunPython(create_groups)
    ]

    