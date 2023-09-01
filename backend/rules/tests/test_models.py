from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from random import randint, choice

from rules import models

class ModelTest(TestCase):
    fixtures = ['test_user']

    test_action = choice(models.Rule.RULE_ACTION_CHOICES)[0]
    test_protocol = choice(models.Rule.RULE_PROTOCOL_CHOICES)[0]
    test_status = choice(models.Rule.RULE_STATUS_CHOICES)[0]
    requester = choice(['Jakob', 'Susi', 'Hansi', 'Lisa'])
    user_count = User.objects.all().count()
    created_by = User.objects.get(id=randint(1, user_count))
    last_updated_by = User.objects.get(id=randint(1, user_count))
    any_str = 'any'

    def test_create_firewall_object(self):
        firewall_object = models.FirewallObject.objects.create(
            hostname = 'FirewallX',
            vendor = 'Checkpoint'
        )
        self.assertIsInstance(firewall_object, models.FirewallObject)
        self.assertEqual(str(firewall_object), 'FirewallX')

    def test_create_rule(self):
        rule = models.Rule.objects.create(
            action = self.test_action,
            protocol = self.test_protocol,
            source_name = self.any_str,
            destination_name = self.any_str,
            status = self.test_status,
            requester = self.requester,
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        self.assertIsInstance(rule, models.Rule)
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
        self.assertEqual(rule.firewalls.all().count(), 0)
        self.assertIsNone(rule.notes)   
        self.assertFalse(rule.is_deleted)

    def test_rule_soft_deleted(self):
        rule = models.Rule.objects.create(
            protocol = self.test_protocol,
            source_name = self.any_str,
            destination_name = self.any_str,
            status = self.test_status,
            requester = self.requester,
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        self.assertFalse(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.last_updated_by)
        rule.soft_deleted(update_user=self.created_by)
        self.assertTrue(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.created_by)

    def test_rule_restore(self):
        rule = models.Rule.objects.create(
            protocol = self.test_protocol,
            source_name = self.any_str,
            destination_name = self.any_str,
            status = self.test_status,
            requester = self.requester,
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        self.assertFalse(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.last_updated_by)
        rule.soft_deleted(update_user=self.created_by)
        self.assertTrue(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.created_by)
        rule.restore(update_user=self.last_updated_by)
        self.assertFalse(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.last_updated_by)
