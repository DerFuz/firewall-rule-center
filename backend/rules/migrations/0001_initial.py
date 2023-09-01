# Generated by Django 4.2.4 on 2023-09-01 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rulesetrequests', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FirewallObject',
            fields=[
                ('hostname', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('vendor', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('PER', 'Permit'), ('DEN', 'Deny')], default='PER', max_length=3)),
                ('protocol', models.CharField(choices=[('TCP', 'TCP'), ('UDP', 'UDP'), ('TCPUDP', 'TCP and UDP'), ('ICMP', 'ICMP'), ('IP', 'IP')], max_length=6)),
                ('source_name', models.CharField(max_length=100)),
                ('source_ip_orig', models.CharField(blank=True, max_length=100)),
                ('source_ip_nat', models.CharField(blank=True, max_length=100)),
                ('source_port', models.PositiveIntegerField(blank=True, null=True)),
                ('destination_name', models.CharField(max_length=100)),
                ('destination_ip_orig', models.CharField(blank=True, max_length=100)),
                ('destination_ip_nat', models.CharField(blank=True, max_length=100)),
                ('destination_port', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('REQ', 'Rule requested'), ('REF', 'Rule refused'), ('APR', 'Rule approved'), ('CON', 'Rule configured'), ('TES', 'Rule tested'), ('DEL', 'Rule deleted')], max_length=3)),
                ('requester', models.CharField(max_length=70)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated_on', models.DateTimeField(auto_now=True)),
                ('ticket', models.CharField(blank=True, max_length=20)),
                ('notes', models.CharField(blank=True, max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='rule_created_by', to=settings.AUTH_USER_MODEL)),
                ('firewalls', models.ManyToManyField(related_name='rule_firewalls', to='rules.firewallobject')),
                ('last_updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='rule_last_updated_by', to=settings.AUTH_USER_MODEL)),
                ('rule_set_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rule_rule_set_request', to='rulesetrequests.rulesetrequest')),
            ],
        ),
    ]
