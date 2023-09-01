from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from datetime import datetime
from random import randint, choice

from rulesetrequests import models

class ModelTest(TestCase):
    fixtures = ['test_user']

    user_count = User.objects.all().count()
    created_by = User.objects.get(id=randint(1, user_count))
    last_updated_by = User.objects.get(id=randint(1, user_count))

    def test_create_rulesetrequest(self):
        rule_set_request = models.RuleSetRequest.objects.create(
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        try:
            rule_set_request.full_clean()
        except Exception as e:
            self.fail(f'full_clean() raised an exception: {e}')

        self.assertIsInstance(rule_set_request, models.RuleSetRequest)
        self.assertEqual(rule_set_request.status, models.RuleSetRequest.REQUESTED)
        self.assertIsNone(rule_set_request.approver)
        self.assertIsInstance(rule_set_request.created_on, datetime)
        self.assertLessEqual(rule_set_request.created_on, timezone.now())
        self.assertEqual(rule_set_request.created_by, self.created_by)
        self.assertIsInstance(rule_set_request.last_updated_on, datetime)
        self.assertLessEqual(rule_set_request.last_updated_on, timezone.now())
        self.assertEqual(rule_set_request.last_updated_by, self.last_updated_by)

    def test_rulesetrequest_illegal_choices(self):
        rule_set_request = models.RuleSetRequest.objects.create(
            status = 'XYZ',
            created_by = self.created_by,
            last_updated_by = self.last_updated_by
        )

        with self.assertRaises(ValidationError):
            rule_set_request.full_clean()