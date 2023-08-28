# Generated by Django 4.2.4 on 2023-08-26 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RuleAction',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('display', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RuleProtocol',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('display', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RuleStatus',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('display', models.CharField(max_length=10)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=100)),
                ('source_ip_orig', models.CharField(blank=True, max_length=100, null=True)),
                ('source_ip_nat', models.CharField(blank=True, max_length=100, null=True)),
                ('source_port', models.PositiveIntegerField(null=True)),
                ('destination_name', models.CharField(max_length=100)),
                ('destination_ip_orig', models.CharField(blank=True, max_length=100, null=True)),
                ('destination_ip_nat', models.CharField(blank=True, max_length=100, null=True)),
                ('destination_port', models.PositiveIntegerField(null=True)),
                ('requester', models.CharField(max_length=70)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=100)),
                ('last_updated_on', models.DateTimeField(auto_now=True)),
                ('last_updated_by', models.CharField(max_length=100)),
                ('ticket', models.CharField(blank=True, max_length=20, null=True)),
                ('firewalls', models.JSONField(null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('action', models.ForeignKey(default='PER', on_delete=django.db.models.deletion.PROTECT, to='rules.ruleaction')),
                ('protocol', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rules.ruleprotocol')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rules.rulestatus')),
            ],
        ),
    ]