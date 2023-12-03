# Generated by Django 4.2.6 on 2023-12-03 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='HistoricalFirewallObject',
            fields=[
                ('hostname', models.CharField(db_index=True, max_length=50)),
                ('vendor', models.CharField(max_length=50)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical firewall object',
                'verbose_name_plural': 'historical firewall objects',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
