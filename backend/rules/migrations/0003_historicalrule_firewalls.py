# Generated by Django 4.2.4 on 2023-10-02 19:11

from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0002_historicalrule_historicalfirewallobject'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRule_firewalls',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('m2m_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('firewallobject', models.ForeignKey(blank=True, db_constraint=False, db_tablespace='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='rules.firewallobject')),
                ('history', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='rules.historicalrule')),
                ('rule', models.ForeignKey(blank=True, db_constraint=False, db_tablespace='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='rules.rule')),
            ],
            options={
                'verbose_name': 'HistoricalRule_firewalls',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
