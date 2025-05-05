import unittest
from unittest.mock import patch, MagicMock
from src.cloud_ip_ranges import CloudIPRanges


class TestCDNs(unittest.TestCase):
    def setUp(self):
        self.formats = {'json', 'csv'}
        self.cloud_ip_ranges = CloudIPRanges(self.formats)

    @patch('requests.get')
    def test_transform_cloudflare(self, mock_get):
        """Test Cloudflare transformation."""
        mock_response_v4 = MagicMock()
        mock_response_v4.text = "1.1.1.0/24"
        mock_response_v6 = MagicMock()
        mock_response_v6.text = "2606:4700:4700::/48"
        mock_get.side_effect = [mock_response_v4, mock_response_v6]

        result = self.cloud_ip_ranges._transform_cloudflare([mock_response_v4, mock_response_v6])
        self.assertEqual(result["provider"], "Cloudflare")
        self.assertEqual(result["ipv4"], ["1.1.1.0/24"])
        self.assertEqual(result["ipv6"], ["2606:4700:4700::/48"])

    @patch('requests.get')
    def test_transform_fastly(self, mock_get):
        """Test Fastly transformation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "addresses": ["1.2.3.0/24"],
            "ipv6_addresses": ["2001:db8::/32"]
        }
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_fastly([mock_response])
        self.assertEqual(result["provider"], "Fastly")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_zscaler(self, mock_get):
        """Test Zscaler transformation."""
        mock_responses = [
            MagicMock(),  # Required data
            MagicMock()   # Recommended data
        ]
        
        # Required data
        mock_responses[0].json.return_value = {
            "hubPrefixes": ["1.2.3.0/24", "2001:db8::/32"]
        }
        
        # Recommended data
        mock_responses[1].json.return_value = {
            "hubPrefixes": ["1.2.3.1/24", "2001:db8:1::/32"]
        }
        
        mock_get.side_effect = mock_responses

        result = self.cloud_ip_ranges._transform_zscaler(mock_responses)
        self.assertEqual(result["provider"], "Zscaler")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24", "1.2.3.1/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32", "2001:db8:1::/32"])

    @patch('requests.get')
    def test_transform_akamai(self, mock_get):
        """Test Akamai transformation."""
        mock_response = MagicMock()
        mock_response.content = b"1.2.3.0/24\n2001:db8::/32"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_akamai([mock_response])
        self.assertEqual(result["provider"], "Akamai")
        self.assertEqual(len(result["ipv4"]), 1)
        self.assertEqual(len(result["ipv6"]), 1)
        self.assertIn("1.2.3.0/24", result["ipv4"])
        self.assertIn("2001:db8::/32", result["ipv6"])
