from django.db import models
from django.db.models import Q
from simple_history.models import HistoricalRecords

class FirewallObjectQuerySet(models.QuerySet):
    def search(self, query) -> models.QuerySet:
        lookup = Q(hostname__in = query)
        qs = self.filter(lookup)
        return qs
    
    
class FirewallObjectManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> FirewallObjectQuerySet:
        return FirewallObjectQuerySet(self.model, using=self._db)
    
    def search(self, query) -> FirewallObjectQuerySet:
        return self.get_queryset().search(query)


class FirewallObject(models.Model):
    hostname = models.CharField(max_length=50, primary_key=True)
    vendor = models.CharField(max_length=50)
    # historical records
    history = HistoricalRecords()
    
    objects = FirewallObjectManager()

    def __str__(self) -> str:
        return self.hostname