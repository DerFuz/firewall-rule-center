from django.test import TestCase

from rules import serializers
from rules import models

class SerializersTest(TestCase):
    fixtures = ['defaults']

    test_action = models.RuleAction.objects.filter(code = 'PER').first()
    test_protocol = models.RuleProtocol.objects.filter(code = 'TCP').first()
    test_status = models.RuleStatus.objects.filter(code = 'UNK').first()
    requester = 'Hansi'
    created_by = 'Seppi'
    last_updated_by = 'Gerti'
    any_str = 'any'

    print(test_action)

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
                'created_by': self.created_by,
                'last_updated_by': self.last_updated_by,
            }

            serializer = serializers.RuleSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f'Expected {ip} to be valid.')

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
                'created_by': self.created_by,
                'last_updated_by': self.last_updated_by,
            }
            serializer = serializers.RuleSerializer(data=data)
            self.assertFalse(serializer.is_valid(), f'Expected {ip} to be invalid.')
