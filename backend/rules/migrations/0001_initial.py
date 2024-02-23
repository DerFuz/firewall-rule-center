# Generated by Django 4.2.6 on 2024-02-23 21:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('firewalls', '0001_initial'),
        ('rulesetrequests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRule',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('action', models.CharField(choices=[('PER', 'Permit'), ('DEN', 'Deny')], max_length=3)),
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
                ('created_on', models.DateTimeField(blank=True, editable=False)),
                ('last_updated_on', models.DateTimeField(blank=True, editable=False)),
                ('ticket', models.CharField(blank=True, max_length=20)),
                ('notes', models.CharField(blank=True, max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(blank=True, db_constraint=False, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('rule_set_request', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='rulesetrequests.rulesetrequest')),
            ],
            options={
                'verbose_name': 'historical rule',
                'verbose_name_plural': 'historical rules',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('PER', 'Permit'), ('DEN', 'Deny')], max_length=3)),
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
                ('firewalls', models.ManyToManyField(related_name='rule_firewalls', to='firewalls.firewallobject')),
                ('last_updated_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='rule_last_updated_by', to=settings.AUTH_USER_MODEL)),
                ('rule_set_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rule_rule_set_request', to='rulesetrequests.rulesetrequest')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalRule_firewalls',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('m2m_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('firewallobject', models.ForeignKey(blank=True, db_constraint=False, db_tablespace='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='firewalls.firewallobject')),
                ('history', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='rules.historicalrule')),
                ('rule', models.ForeignKey(blank=True, db_constraint=False, db_tablespace='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='rules.rule')),
            ],
            options={
                'verbose_name': 'HistoricalRule_firewalls',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
