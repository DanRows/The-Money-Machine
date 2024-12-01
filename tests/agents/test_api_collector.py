import unittest
from unittest.mock import patch, Mock
import requests
from datetime import datetime
from src.agents.data_collectors.api_collector import APIDataCollector

class TestAPIDataCollector(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_config = {
            "source_name": "test_api",
            "base_url": "https://api.example.com/data",
            "headers": {"Authorization": "Bearer token"},
            "params": {"param1": "value1"}
        }
        self.collector = APIDataCollector(self.valid_config)

    @patch('requests.Session')
    def test_connect_success(self, mock_session):
        mock_instance = Mock()
        mock_instance.get.return_value.raise_for_status.return_value = None
        mock_session.return_value = mock_instance
        
        self.assertTrue(self.collector.connect())

    @patch('requests.Session')
    def test_connect_failure(self, mock_session):
        mock_instance = Mock()
        mock_instance.get.side_effect = requests.exceptions.RequestException()
        mock_session.return_value = mock_instance
        
        self.assertFalse(self.collector.connect())

    @patch('requests.Session')
    def test_fetch_data_success(self, mock_session):
        mock_instance = Mock()
        mock_instance.get.return_value.json.return_value = {"key": "value"}
        mock_session.return_value = mock_instance
        
        self.collector.session = mock_instance
        result = self.collector.fetch_data()
        self.assertEqual(result, {"key": "value"})

    @patch('requests.Session')
    def test_process_input_success(self, mock_session):
        mock_instance = Mock()
        mock_instance.get.return_value.raise_for_status.return_value = None
        mock_instance.get.return_value.json.return_value = {"key": "value"}
        mock_session.return_value = mock_instance
        
        result = self.collector.process_input()
        
        self.assertEqual(result["data"], {"key": "value"})
        self.assertEqual(result["metadata"]["source_name"], "test_api")
        self.assertEqual(result["metadata"]["status"], "success")
        self.assertIsNone(result["metadata"]["error_message"])

if __name__ == '__main__':
    unittest.main() 