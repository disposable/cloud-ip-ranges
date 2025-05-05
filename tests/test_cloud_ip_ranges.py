import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.cloud_ip_ranges import CloudIPRanges
import io
import zipfile
import time
import requests


class TestCloudIPRanges(unittest.TestCase):
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
    def test_transform_hackertarget(self, mock_get):
        """Test HackerTarget transformation."""
        mock_response = MagicMock()
        mock_response.text = "# AS55293 A2 Hosting\n1.2.3.0/24\n2001:db8::/32"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_hackertarget([mock_response], "a2hosting")
        self.assertEqual(result["provider"], "A2Hosting")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    def test_transform_hackertarget_invalid_data(self):
        """Test HackerTarget transformation with invalid data."""
        mock_response = MagicMock()
        mock_response.text = "# Invalid data"
        result = self.cloud_ip_ranges._transform_hackertarget([mock_response], "a2hosting")
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
    def test_transform_digitalocean(self, mock_get):
        """Test DigitalOcean transformation."""
        mock_response = MagicMock()
        mock_response.text = "1.2.3.0/24,example.com\n2001:db8::/32,example.com"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_digitalocean([mock_response])
        self.assertEqual(result["provider"], "Digitalocean")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_linode(self, mock_get):
        """Test Linode transformation."""
        mock_response = MagicMock()
        mock_response.text = "# Linode IP Ranges\n1.2.3.0/24\n2001:db8::/32"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_linode([mock_response])
        self.assertEqual(result["provider"], "Linode")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_apple_icloud(self, mock_get):
        """Test Apple iCloud transformation."""
        mock_response = MagicMock()
        mock_response.text = "1.2.3.0/24,example.com\n2001:db8::/32,example.com"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_apple_icloud([mock_response])
        self.assertEqual(result["provider"], "Apple Icloud")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_zscaler(self, mock_get):
        """Test Zscaler transformation."""
        mock_response_required = MagicMock()
        mock_response_required.json.return_value = {
            "hubPrefixes": ["1.2.3.0/24"]
        }
        mock_response_recommended = MagicMock()
        mock_response_recommended.json.return_value = {
            "hubPrefixes": ["2001:db8::/32"]
        }
        mock_get.side_effect = [mock_response_required, mock_response_recommended]

        result = self.cloud_ip_ranges._transform_zscaler([mock_response_required, mock_response_recommended])
        self.assertEqual(result["provider"], "Zscaler")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

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
    def test_transform_vultr(self, mock_get):
        """Test Vultr transformation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "subnets": [
                {"ip_prefix": "1.2.3.0/24"},
                {"ip_prefix": "2001:db8::/32"}
            ]
        }
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_vultr([mock_response])
        self.assertEqual(result["provider"], "Vultr")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_github(self, mock_get):
        """Test GitHub transformation."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "hooks": ["1.2.3.0/24"],
            "web": ["2001:db8::/32"]
        }
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_github([mock_response])
        self.assertEqual(result["provider"], "Github")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_microsoft_azure(self, mock_get):
        """Test Microsoft Azure transformation."""
        # First response is the HTML page
        mock_html_response = MagicMock()
        mock_html_response.text = """
        <html>
            <a href="https://download.microsoft.com/download/1/2/3/azure.json">
                Download
            </a>
        </html>
        """
        
        # Second response is the JSON file
        mock_json_response = MagicMock()
        mock_json_response.json.return_value = {
            "values": [
                {
                    "properties": {
                        "addressPrefixes": ["1.2.3.0/24", "2001:db8::/32"]
                    }
                }
            ]
        }
        
        # Set up the mock to return different responses
        mock_get.side_effect = [mock_json_response]
        
        # Mock the actual requests.get call within the method
        with patch('requests.get') as mock_get_inner:
            mock_get_inner.return_value = mock_json_response
            result = self.cloud_ip_ranges._transform_microsoft_azure([mock_html_response])
            self.assertEqual(result["provider"], "Microsoft Azure")
            self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
            self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_akamai(self, mock_get):
        """Test Akamai transformation."""
        # Create a mock ZIP file with two files
        mock_zip_data = io.BytesIO()
        with zipfile.ZipFile(mock_zip_data, 'w') as zipf:
            zipf.writestr('akamai_ipv4_CIDRs.txt', '1.2.3.0/24')
            zipf.writestr('akamai_ipv6_CIDRs.txt', '2001:db8::/32')
        mock_zip_data.seek(0)

        mock_response = MagicMock()
        mock_response.content = mock_zip_data.getvalue()
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_akamai([mock_response])
        self.assertEqual(result["provider"], "Akamai")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

if __name__ == '__main__':
    unittest.main()
