import unittest
from unittest.mock import patch, MagicMock
from src.cloud_ip_ranges import CloudIPRanges


class TestHostingProviders(unittest.TestCase):
    def setUp(self):
        self.formats = {'json', 'csv'}
        self.cloud_ip_ranges = CloudIPRanges(self.formats)

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
        mock_response.text = "# Linode IP Ranges\n1.2.3.0/24,example.com\n2001:db8::/32,example.com"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_linode([mock_response])
        self.assertEqual(result["provider"], "Linode")
        self.assertEqual(result["ipv4"], ["1.2.3.0/24"])
        self.assertEqual(result["ipv6"], ["2001:db8::/32"])

    @patch('requests.get')
    def test_transform_hackertarget(self, mock_get):
        """Test HackerTarget transformation."""
        mock_response = MagicMock()
        mock_response.text = "# AS12345 Softlayer IBM\nAS12345 1.2.3.0/24\nAS12345 2001:db8::/32"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_hackertarget([mock_response], "softlayer_ibm")
        self.assertEqual(result["provider"], "Softlayer Ibm")
        self.assertEqual(len(result["ipv4"]), 1)
        self.assertEqual(len(result["ipv6"]), 1)
        self.assertIn("1.2.3.0/24", result["ipv4"])
        self.assertIn("2001:db8::/32", result["ipv6"])

    @patch('requests.get')
    def test_transform_hackertarget_invalid_data(self, mock_get):
        """Test HackerTarget invalid data handling."""
        mock_response = MagicMock()
        mock_response.text = "Invalid data"
        mock_get.return_value = mock_response

        result = self.cloud_ip_ranges._transform_hackertarget([mock_response], "softlayer_ibm")
        self.assertEqual(result["provider"], "Softlayer Ibm")
        self.assertEqual(result["ipv4"], [])
        self.assertEqual(result["ipv6"], [])
