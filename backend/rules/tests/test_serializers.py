from django.test import TestCase
from django.contrib.auth.models import User
from random import randint, choice

from rules import serializers
from rules import models

class SerializersTest(TestCase):
    fixtures = ['defaults', 'test_user', 'test_firewallobjects']

    test_action = models.RuleAction.objects.filter(code = 'PER').first()
    test_protocol = models.RuleProtocol.objects.filter(code = 'TCP').first()
    test_status = models.RuleStatus.objects.filter(code = 'UNK').first()
    test_firewalls = list(models.FirewallObject.objects.values('hostname'))
    user_count = User.objects.all().count()
    requester = choice(['Jakob', 'Susi', 'Hansi', 'Lisa'])
    any_str = 'any'

    def test_ip_validators(self):
        # Test valid IP addresses
        valid_ips = [
            '192.168.0.1',
            '10.0.0.1',
            '0.0.0.0/0',
            '::1', 
            '2001::affe',
            '::/0',
            '2001::10/126'
        ]
        
        for ip in valid_ips:
            data = {
                'source_ip_orig': ip,
                'source_ip_nat': ip,
                'destination_ip_orig': ip,
                'destination_ip_nat': ip,
                'protocol': "TCP",
                'source_name': self.any_str,
                'destination_name': self.any_str,
                'status': "UNK",
                'requester': self.requester,
                'firewalls': self.test_firewalls,
            }

            serializer = serializers.RuleSerializer(data=data)
            self.assertTrue(serializer.is_valid(raise_exception=True), f'Expected {ip} to be valid.')

        # Test invalid IP addresses
        invalid_ips = [
            'invalid_ip',
            '256.0.0.1',
            '2001::12/126',
            '192.168.0.1/24',
            '192.168.000.10',
            '',
            '2001::ab::1',
            '2001::/129'
        ]

        for ip in invalid_ips:
            data = {
                'source_ip_orig': ip,
                'source_ip_nat': ip,
                'destination_ip_orig': ip,
                'destination_ip_nat': ip,
                'protocol': "TCP",
                'source_name': self.any_str,
                'destination_name': self.any_str,
                'status': "UNK",
                'requester': self.requester,
                'firewalls': self.test_firewalls,
            }
            serializer = serializers.RuleSerializer(data=data)
            self.assertFalse(serializer.is_valid(raise_exception=True), f'Expected {ip} to be invalid.')


    def test_ip_mutual_exclusion(self):
        standard_data = {
            'protocol': "TCP",
            'source_name': self.any_str,
            'destination_name': self.any_str,
            'status': "UNK",
            'requester': self.requester,
            'firewalls': self.test_firewalls,
        }
        
        # from itertools import product
        # test_ip = '10.0.0.1/32'
        # fields = ['source_ip_orig', 'source_ip_nat', 'destination_ip_orig', 'destination_ip_nat']
        # print([list(zip(fields, x)) for x in product([test_ip, None], repeat=len(fields))])

        possibilities = [
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', '10.0.0.1/32')],   # legal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', None)],            # legal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', None), ('destination_ip_nat', '10.0.0.1/32')],            # legal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', None), ('destination_ip_nat', None)],                     # illegal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', None), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', '10.0.0.1/32')],            # legal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', None), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', None)],                     # legal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', None), ('destination_ip_orig', None), ('destination_ip_nat', '10.0.0.1/32')],                     # legal
            [('source_ip_orig', '10.0.0.1/32'), ('source_ip_nat', None), ('destination_ip_orig', None), ('destination_ip_nat', None)],                              # illegal
            [('source_ip_orig', None), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', '10.0.0.1/32')],            # legal
            [('source_ip_orig', None), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', None)],                     # legal
            [('source_ip_orig', None), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', None), ('destination_ip_nat', '10.0.0.1/32')],                     # legal
            [('source_ip_orig', None), ('source_ip_nat', '10.0.0.1/32'), ('destination_ip_orig', None), ('destination_ip_nat', None)],                              # illegal
            [('source_ip_orig', None), ('source_ip_nat', None), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', '10.0.0.1/32')],                     # illegal
            [('source_ip_orig', None), ('source_ip_nat', None), ('destination_ip_orig', '10.0.0.1/32'), ('destination_ip_nat', None)],                              # illegal
            [('source_ip_orig', None), ('source_ip_nat', None), ('destination_ip_orig', None), ('destination_ip_nat', '10.0.0.1/32')],                              # illegal
            [('source_ip_orig', None), ('source_ip_nat', None), ('destination_ip_orig', None), ('destination_ip_nat', None)]                                        # illegal
        ]        
        for possibility in possibilities:
            test_data = dict()
            for (name, value) in possibility:
                if value is not None:
                    test_data[name] = value

            serializer = serializers.RuleSerializer(data={**standard_data, **test_data})

            if (test_data.get('source_ip_orig') or test_data.get('source_ip_nat')) \
                and (test_data.get('destination_ip_orig') or test_data.get('destination_ip_nat')):
                self.assertTrue(serializer.is_valid(raise_exception=True), f'Expected testset to be valid.')
            else:
                self.assertFalse(serializer.is_valid(raise_exception=True), f'Expected testset to be invalid.')
