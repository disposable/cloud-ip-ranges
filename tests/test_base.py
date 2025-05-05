import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.cloud_ip_ranges import CloudIPRanges
import io
import zipfile
import requests


class TestBase(unittest.TestCase):
    def setUp(self):
        self.formats = {'json', 'csv'}
        self.cloud_ip_ranges = CloudIPRanges(self.formats)

    def test_transform_base(self):
        """Test base transformation method."""
        result = self.cloud_ip_ranges._transform_base("aws")
        self.assertEqual(result["provider"], "Aws")
        self.assertEqual(result["source"], "https://ip-ranges.amazonaws.com/ip-ranges.json")
        self.assertIn("last_updated", result)
        self.assertEqual(result["ipv4"], [])
        self.assertEqual(result["ipv6"], [])

    def test_error_handling_request_timeout(self):
        """Test request timeout handling."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout
        
        result = self.cloud_ip_ranges._transform_aws([mock_response])
        self.assertEqual(result["ipv4"], [])
        self.assertEqual(result["ipv6"], [])
        self.assertNotIn("createDate", result)
        self.assertIn("last_updated", result)
        self.assertEqual(result["provider"], "Aws")
        self.assertEqual(result["source"], "https://ip-ranges.amazonaws.com/ip-ranges.json")

    def test_error_handling_invalid_ip(self):
        """Test invalid IP address handling."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "createDate": "2025-05-04",
            "prefixes": [{"ip_prefix": "invalid_ip"}],
            "ipv6_prefixes": [{"ipv6_prefix": "not_an_ip"}]
        }
        
        result = self.cloud_ip_ranges._transform_aws([mock_response])
        self.assertEqual(result["ipv4"], ["invalid_ip"])
        self.assertEqual(result["ipv6"], ["not_an_ip"])
        self.assertEqual(result["last_updated"], "2025-05-04")
