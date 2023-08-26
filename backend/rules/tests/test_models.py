from django.test import TestCase
from django.utils import timezone

from rules import models

class ModelTest(TestCase):
    fixtures = ["defaults"]

    test_action = models.RuleAction.objects.filter(code = 'PER').first()
    test_protocol = models.RuleProtocol.objects.filter(code = 'TCP').first()
    test_status = models.RuleStatus.objects.filter(code = 'UNK').first()
    requester = 'Hansi'
    created_by = 'Seppi'
    last_updated_by = 'Gerti'
    any_str = 'any'

    def test_create_rule_action(self):
        rule_action = models.RuleAction.objects.create(
            code = 'TEST',
            display = 'Testing',
            description = 'This is the testing action'
        )
        self.assertIsInstance(rule_action, models.RuleAction)

    def test_create_rule_protocol(self):
        rule_protocol = models.RuleProtocol.objects.create(
            code = 'ICMP',
            display = 'Icmp',
            description = 'Internet Control Message Protocol'
        )
        self.assertIsInstance(rule_protocol, models.RuleProtocol)

    def test_create_rule_status(self):
        rule_status = models.RuleStatus.objects.create(
            code = 'XX',
            display = 'Xxxx',
            description = 'Exiting :)'
        )
        self.assertIsInstance(rule_status, models.RuleStatus)

    def test_create_rule(self):
        rule = models.Rule.objects.create(
            protocol = self.test_protocol,
            source_name = self.any_str,
            destination_name = self.any_str,
            status = self.test_status,
            requester = self.requester,
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        self.assertEqual(rule.action, self.test_action)
        self.assertEqual(rule.protocol, self.test_protocol)
        self.assertEqual(rule.source_name, self.any_str)
        self.assertIsNone(rule.source_ip_orig)
        self.assertIsNone(rule.source_ip_nat)
        self.assertIsNone(rule.source_port)
        self.assertEqual(rule.destination_name, self.any_str)
        self.assertIsNone(rule.destination_ip_orig)
        self.assertIsNone(rule.destination_ip_nat)
        self.assertIsNone(rule.destination_port)
        self.assertEqual(rule.status, self.test_status)
        self.assertEqual(rule.requester, self.requester)
        self.assertLessEqual(rule.created_on, timezone.now())
        self.assertEqual(rule.created_by, self.created_by)
        self.assertLessEqual(rule.last_updated_on, timezone.now())
        self.assertEqual(rule.last_updated_by, self.last_updated_by)
        self.assertIsNone(rule.ticket)
        self.assertIsNone(rule.firewalls)
        self.assertIsNone(rule.notes)   
        self.assertFalse(rule.is_deleted)