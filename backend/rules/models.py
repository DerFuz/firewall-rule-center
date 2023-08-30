from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL # auth.user

class RuleAction(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    display = models.CharField(max_length=10)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.display} ({self.description})'


class RuleProtocol(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    display = models.CharField(max_length=10)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.display} ({self.description})'


class RuleStatus(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    display = models.CharField(max_length=10)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.display} ({self.description})'


class FirewallObject(models.Model):
    hostname = models.CharField(max_length=50, primary_key=True)
    vendor = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.hostname


class RuleQuerySet(models.QuerySet):
    def is_deleted(self) -> models.QuerySet:
        return self.filter(is_deleted=True)
    
    def is_not_deleted(self) -> models.QuerySet:
        return self.filter(is_deleted=False)
    
    def search(self, query, user=None) -> models.QuerySet:
        lookup = Q(source_ip_orig__icontains = query) | Q(destination_ip_orig__icontains = query)
        qs = self.is_not_deleted().filter(lookup)
        return qs


class RuleManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> RuleQuerySet:
        return RuleQuerySet(self.model, using=self._db)
    
    #def search(self, query, user=None) -> RuleQuerySet:
    #    return self.get_queryset().search(query, user=user)
    
    def exclude_deleted(self) -> RuleQuerySet:
        return self.get_queryset().is_not_deleted()
    
    
class Rule(models.Model):
    # RuleAction
    action = models.ForeignKey(RuleAction, default='PER', on_delete=models.PROTECT)
    
    # RuleProtocol
    protocol = models.ForeignKey(RuleProtocol, on_delete=models.PROTECT)

    # Source
    # TODO reference object in the future maybe?
    source_name = models.CharField(max_length=100)
    source_ip_orig = models.CharField(max_length=100, blank=True, null=True)
    source_ip_nat = models.CharField(max_length=100, blank=True, null=True)
    source_port = models.PositiveIntegerField(null=True)

    # Destination
    destination_name = models.CharField(max_length=100)
    destination_ip_orig = models.CharField(max_length=100, blank=True, null=True)
    destination_ip_nat = models.CharField(max_length=100, blank=True, null=True)
    destination_port = models.PositiveIntegerField(null=True)

    # RuleStatus
    status = models.ForeignKey(RuleStatus, on_delete=models.PROTECT)

    # Requester of the rule
    requester = models.CharField(max_length=70)
    
    # Rule entry creation timestamp
    created_on = models.DateTimeField(auto_now_add=True)

    # Creator of this rule entry
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.PROTECT)

    # Rule entry update timestamp
    last_updated_on = models.DateTimeField(auto_now=True)

    # Last user that updated this rule entry
    last_updated_by = models.ForeignKey(User, related_name='last_updated_by', on_delete=models.PROTECT)

    # Ticket number, etc
    ticket = models.CharField(max_length=20, blank=True, null=True)

    # list of firewalls
    firewalls = models.ManyToManyField(to=FirewallObject, related_name='rule_firewalls')

    # Notes about this entry
    notes = models.CharField(max_length=200, blank=True, null=True)

    # mark rule entry as deleted
    is_deleted = models.BooleanField(default=False)

    objects = RuleManager()

    def __str__(self) -> str:
        return f'Rule: [{self.pk}], \
from [{self.source_name} - {self.source_ip_orig}/{self.source_port}] \
to [{self.destination_name} - {self.destination_ip_orig}/{self.destination_port}] \
requested by [{self.requester}] in status [{self.status}]'

    def soft_deleted(self, update_user):
        self.is_deleted = True
        self.last_updated_by = update_user
        self.save()

    def restore(self, update_user):
        self.is_deleted = False
        self.last_updated_by = update_user
        self.save()