from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


from datetime import datetime
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

        try:
            firewall_object.full_clean()
        except Exception as e:
            self.fail(f'full_clean() raised an exception: {e}')

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

        try:
            rule.full_clean()
        except Exception as e:
            self.fail(f'full_clean() raised an exception: {e}')

        self.assertIsInstance(rule, models.Rule)
        self.assertEqual(rule.action, self.test_action)
        self.assertEqual(rule.protocol, self.test_protocol)
        self.assertEqual(rule.source_name, self.any_str)
        self.assertEqual(rule.source_ip_orig, '')
        self.assertEqual(rule.source_ip_nat, '')
        self.assertIsNone(rule.source_port)
        self.assertEqual(rule.destination_name, self.any_str)
        self.assertEqual(rule.destination_ip_orig, '')
        self.assertEqual(rule.destination_ip_nat, '')
        self.assertIsNone(rule.destination_port)
        self.assertEqual(rule.status, self.test_status)
        self.assertEqual(rule.requester, self.requester)
        self.assertIsInstance(rule.created_on, datetime)
        self.assertLessEqual(rule.created_on, timezone.now())
        self.assertEqual(rule.created_by, self.created_by)
        self.assertIsInstance(rule.last_updated_on, datetime)
        self.assertLessEqual(rule.last_updated_on, timezone.now())
        self.assertEqual(rule.last_updated_by, self.last_updated_by)
        self.assertEqual(rule.ticket, '')
        self.assertIsNone(rule.rule_set_request)
        self.assertEqual(rule.firewalls.all().count(), 0)
        self.assertEqual(rule.notes, '')   
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

        try:
            rule.full_clean()
        except Exception as e:
            self.fail(f'full_clean() raised an exception: {e}')

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
        
        try:
            rule.full_clean()
        except Exception as e:
            self.fail(f'full_clean() raised an exception: {e}')

        self.assertFalse(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.last_updated_by)
        rule.soft_deleted(update_user=self.created_by)
        self.assertTrue(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.created_by)
        rule.restore(update_user=self.last_updated_by)
        self.assertFalse(rule.is_deleted)
        self.assertEqual(rule.last_updated_by, self.last_updated_by)

    def test_rule_illegal_choices(self):
        rule = models.Rule.objects.create(
            protocol = self.test_protocol,
            source_name = self.any_str,
            destination_name = self.any_str,
            status = self.test_status,
            requester = self.requester,
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        try:
            rule.full_clean()
        except Exception as e:
            self.fail(f'full_clean() raised an exception: {e}')

        with self.assertRaises(ValidationError, msg='Accepting illegal value for rule.action'):
            rule.action = 'ILLEGAL'
            rule.full_clean()

        rule.action = self.test_action
        rule.full_clean()

        with self.assertRaises(ValidationError, msg='Accepting illegal value for rule.protocol'):
             rule.protocol = 'ILLEGAL'
             rule.full_clean()

        rule.protocol = self.test_protocol
        rule.full_clean()

        with self.assertRaises(ValidationError, msg='Accepting illegal value for rule.status'):
            rule.status = 'ILLEGAL'
            rule.full_clean()