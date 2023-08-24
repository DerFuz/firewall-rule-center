from django.db import models

class Rule(models.Model):
    # TODO make action a foreign key or ENUM?
    #action = models.ForeignKey(Action, default=, null=True, on_delete=models.SET_NULL)
    PERMIT = 'P'
    DENY = 'D'
    RULE_ACTION_CHOICES = [
        (PERMIT, 'Permit'),
        (DENY, 'Deny')
    ]
    action = models.CharField(max_length=1, choices=RULE_ACTION_CHOICES, default=PERMIT)
    
    # TODO source and destination create a validator
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    
    # TODO make protocol a foreign key or ENUM?
    protocol = models.CharField(max_length=10)
    
    # TODO Portlist possible?
    port = models.IntegerField()

    # TODO make status a foreign key or ENUM?
    status = models.CharField(max_length=20)

    # TODO user-object?
    requester = models.CharField(max_length=50)