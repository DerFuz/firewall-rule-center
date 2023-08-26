from django.test import TestCase
from django.utils import timezone

from rules import models

class ModelTest(TestCase):
    fixtures = ["defaults"]

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
        test_action = models.RuleAction.objects.filter(code = 'PER').first()
        test_protocol = models.RuleProtocol.objects.filter(code = 'TCP').first()
        test_status = models.RuleStatus.objects.filter(code = 'UNK').first()
        requester = 'Hansi'
        created_by = 'Seppi'
        last_updated_by = 'Gerti'
        any_str = 'any'
        rule = models.Rule.objects.create(
            protocol = test_protocol,
            source_name = any_str,
            destination_name = any_str,
            status = test_status,
            requester = requester,
            created_by = created_by,
            last_updated_by = last_updated_by
        )

        self.assertEqual(rule.action, test_action)
        self.assertEqual(rule.protocol, test_protocol)
        self.assertEqual(rule.source_name, any_str)
        self.assertIsNone(rule.source_ip_orig)
        self.assertIsNone(rule.source_ip_nat)
        self.assertIsNone(rule.source_port)
        self.assertEqual(rule.destination_name, any_str)
        self.assertIsNone(rule.destination_ip_orig)
        self.assertIsNone(rule.destination_ip_nat)
        self.assertIsNone(rule.destination_port)
        self.assertEqual(rule.status, test_status)
        self.assertEqual(rule.requester, requester)
        self.assertLessEqual(rule.created_on, timezone.now())
        self.assertEqual(rule.created_by, created_by)
        self.assertLessEqual(rule.last_updated_on, timezone.now())
        self.assertEqual(rule.last_updated_by, last_updated_by)
        self.assertIsNone(rule.ticket)
        self.assertIsNone(rule.firewalls)
        self.assertIsNone(rule.notes)   
        self.assertFalse(rule.is_deleted)
