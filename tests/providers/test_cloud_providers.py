import unittest
from unittest.mock import patch, MagicMock
from src.cloud_ip_ranges import CloudIPRanges


class TestCloudProviders(unittest.TestCase):
    def setUp(self):
        self.formats = {'json', 'csv'}
        self.cloud_ip_ranges = CloudIPRanges(self.formats)

    @patch('requests.get')
    def test_transform_aws(self, mock_get):
        """Test AWS transformation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "createDate": "2025-05-04",
            "prefixes": [{"ip_prefix": "1.2.3.0/24"}],
            "ipv6_prefixes": [{"ipv6_prefix": "2001:db8::/32"}]
        }
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_aws([mock_response])
        self.assertEqual(result["provider"], "Aws")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])
        self.assertEqual(result["last_updated"], "2025-05-04")

    @patch('requests.get')
    def test_transform_google_cloud(self, mock_get):
        """Test Google Cloud transformation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "prefixes": [
                {"ipv4Prefix": "1.2.3.0/24"},
                {"ipv6Prefix": "2001:db8::/32"}
            ]
        }
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_google_cloud([mock_response])
        self.assertEqual(result["provider"], "Google Cloud")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_oracle_cloud(self, mock_get):
        """Test Oracle Cloud transformation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "regions": [
                {
                    "cidrs": [
                        {"cidr": "1.2.3.0/24"},
                        {"cidr": "2001:db8::/32"}
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_oracle_cloud([mock_response])
        self.assertEqual(result["provider"], "Oracle Cloud")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_microsoft_azure(self, mock_get):
        """Test Microsoft Azure transformation."""
        mock_response = MagicMock()
        mock_response.text = "<a href='https://download.microsoft.com/data.json'>Download</a>"
        mock_json = MagicMock()
        mock_json.json.return_value = {
            "values": [
                {
                    "properties": {
                        "addressPrefixes": ["1.2.3.0/24"],
                        "platform": "Azure",
                        "systemService": "Service1"
                    }
                },
                {
                    "properties": {
                        "addressPrefixes": ["2001:db8::/32"],
                        "platform": "Azure",
                        "systemService": "Service2"
                    }
                }
            ]
        }
        mock_get.side_effect = [mock_response, mock_json]

        result = self.cloud_ip_ranges._transform_microsoft_azure([mock_response])
        self.assertEqual(result["provider"], "Microsoft Azure")
        self.assertEqual(len(result["ipv4"]), 1)
        self.assertEqual(len(result["ipv6"]), 1)
        self.assertIn("1.2.3.0/24", result["ipv4"])
        self.assertIn("2001:db8::/32", result["ipv6"])
