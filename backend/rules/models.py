from django.db import models
from django.conf import settings
from django.db.models import Q
from simple_history.models import HistoricalRecords
from django.contrib.auth import get_user_model

from rulesetrequests.models import RuleSetRequest
from firewalls.models import FirewallObject

class RuleQuerySet(models.QuerySet):
    def is_deleted(self) -> models.QuerySet:
        return self.filter(is_deleted=True)
    
    def is_not_deleted(self) -> models.QuerySet:
        return self.filter(is_deleted=False)
    
    def filter_by_rule_set_request(self, rule_set_request) -> models.QuerySet:
        return self.filter(rule_set_request=rule_set_request)
    
    # def search(self, query, user=None) -> models.QuerySet:
    #     lookup = Q(source_ip_orig__icontains = query) | Q(destination_ip_orig__icontains = query)
    #     qs = self.is_not_deleted().filter(lookup)
    #     return qs


class RuleManager(models.Manager):
    def get_queryset(self, *args, **kwargs) -> RuleQuerySet:
        return RuleQuerySet(self.model, using=self._db)
    
    #def search(self, query, user=None) -> RuleQuerySet:
    #    return self.get_queryset().search(query, user=user)
    
    def get_rules_from_rule_set_request(self, rule_set_request) -> RuleQuerySet:
        return self.get_queryset().filter_by_rule_set_request(rule_set_request)
    
    def exclude_deleted(self) -> RuleQuerySet:
        return self.get_queryset().is_not_deleted()
    
    
class Rule(models.Model):
    # Action Choices
    PERMIT = 'PER'
    DENY = 'DEN'
    
    RULE_ACTION_CHOICES = [
        (PERMIT, 'Permit'),
        (DENY, 'Deny')
    ]

    # Protocol Choices
    TCP = 'TCP'
    UDP = 'UDP'
    TCP_UDP = 'TCPUDP'
    ICMP = 'ICMP'
    IP = 'IP'
    
    RULE_PROTOCOL_CHOICES = [
        (TCP, 'TCP'),
        (UDP, 'UDP'),
        (TCP_UDP, 'TCP and UDP'),
        (ICMP, 'ICMP'),
        (IP, 'IP'),
    ]

    # Status Choices
    REQUESTED = 'REQ'
    REFUSED = 'REF'
    APPROVED = 'APR'
    CONFIGURED = 'CON'
    TESTED = 'TES'
    DELETED = 'DEL'
    
    RULE_STATUS_CHOICES = [
        (REQUESTED, 'Rule requested'),
        (REFUSED, 'Rule refused'),
        (APPROVED, 'Rule approved'),
        (CONFIGURED, 'Rule configured'),
        (TESTED, 'Rule tested'),
        (DELETED, 'Rule deleted')
    ]


    # Action
    action = models.CharField(max_length=3, choices=RULE_ACTION_CHOICES)
    
    # Protocol
    protocol = models.CharField(max_length=6, choices=RULE_PROTOCOL_CHOICES)

    # Source
    # TODO reference object in the future maybe?
    source_name = models.CharField(max_length=100)
    source_ip_orig = models.CharField(max_length=100, blank=True)
    source_ip_nat = models.CharField(max_length=100, blank=True)
    source_port = models.PositiveIntegerField(blank=True, null=True)

    # Destination
    destination_name = models.CharField(max_length=100)
    destination_ip_orig = models.CharField(max_length=100, blank=True)
    destination_ip_nat = models.CharField(max_length=100, blank=True)
    destination_port = models.PositiveIntegerField(blank=True, null=True)

    # Status
    status = models.CharField(max_length=3, choices=RULE_STATUS_CHOICES)

    # Requester of the rule
    requester = models.CharField(max_length=70)
    
    # Rule entry creation timestamp
    created_on = models.DateTimeField(auto_now_add=True)

    # Creator of this rule entry
    created_by = models.ForeignKey(get_user_model(), related_name='rule_created_by', editable=False, on_delete=models.PROTECT)

    # Rule entry update timestamp
    last_updated_on = models.DateTimeField(auto_now=True)

    # Last user that updated this rule entry
    last_updated_by = models.ForeignKey(get_user_model(), related_name='rule_last_updated_by', editable=False, on_delete=models.PROTECT)

    # Ticket number, etc
    ticket = models.CharField(max_length=20, blank=True)

    # RuleSetRequest
    rule_set_request = models.ForeignKey(RuleSetRequest, related_name='rule_rule_set_request', blank=True, null=True, on_delete=models.SET_NULL)

    # list of firewalls
    firewalls = models.ManyToManyField(to=FirewallObject, related_name='rule_firewalls')

    # Notes about this entry
    notes = models.CharField(max_length=200, blank=True)

    # mark rule entry as deleted
    is_deleted = models.BooleanField(default=False)

    # historical records
    history = HistoricalRecords(m2m_fields=[firewalls])

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
        
    def set_status(self, status, update_user):
        self.status = status
        self.last_updated_by = update_user
        self.save()