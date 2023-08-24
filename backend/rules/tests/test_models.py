from django.test import TestCase

from rules import models

class ModelTest(TestCase):

    def test_create_rule(self):
        rule = models.Rule.objects.create(
            action = 'PERMIT',
            source = '10.0.0.1',
            destination = '8.8.8.8',
            protocol = 'tcp',
            port = '443',
            status = 'active',
            requester = 'Hansi'
        )

        self.assertIsNotNone(rule)

    def test_check_action(self):
        action_str = 'C'
        rule = models.Rule.objects.create(
            action = action_str,
            source = '10.0.0.1',
            destination = '8.8.8.8',
            protocol = 'tcp',
            port = '443',
            status = 'active',
            requester = 'Hansi'
        )

        self.assertEquals(rule.action, action_str)