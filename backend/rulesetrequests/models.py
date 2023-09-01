from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL # auth.user

class RuleSetRequest(models.Model):
    # Status Choices
    REQUESTED = 'REQ'
    REFUSED = 'REF'
    APPROVED = 'APR'
    CONFIGURED = 'CON'
    
    RULESETREQUEST_STATUS_CHOICES = [
        (REQUESTED, 'RuleSetRequest requested'),
        (REFUSED, 'RuleSetRequest refused'),
        (APPROVED, 'RuleSetRequest approved'),
        (CONFIGURED, 'All rules in this RuleSetRequest configured'),
    ]

    # Status
    status = models.CharField(max_length=3, choices=RULESETREQUEST_STATUS_CHOICES, default=REQUESTED)

    # approver of this rulesetrequest entry
    approver = models.ForeignKey(User, related_name='rulesetrequest_approved_by', blank=True, null=True, on_delete=models.PROTECT)

    # RuleSetRequest entry creation timestamp
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Creator of this rulesetrequest entry
    created_by = models.ForeignKey(User, related_name='rulesetrequest_created_by', on_delete=models.PROTECT)

    # RuleSetRequest entry update timestamp
    last_updated_on = models.DateTimeField(auto_now=True)

    # Last user that updated this RuleSetRequest entry
    last_updated_by = models.ForeignKey(User, related_name='rulesetrequest_last_updated_by', on_delete=models.PROTECT)
