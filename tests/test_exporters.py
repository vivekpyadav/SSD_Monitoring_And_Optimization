import unittest
from unittest.mock import patch
import sys
sys.path.append("/home/kalilinux_user/devops/SSD_project")
from src.exporters.json_exporter import save_metrics_to_json, collect_metrics


class TestExporters(unittest.TestCase):
    @patch("builtins.open")
    @patch("json.dump")
    def test_save_metrics_to_json(self, mock_json_dump, mock_open):
        """Test saving metrics to a JSON file."""
        metrics = {"disk": {"Temperature_Celsius": "37"}}
        save_metrics_to_json(metrics)
        mock_open.assert_called_once_with("logs/ssd_metrics.json", "w")
        mock_json_dump.assert_called_once_with(metrics, mock_open.return_value, indent=4)

    @patch("src.monitor.get_smart_data")
    def test_collect_metrics(self, mock_get_smart_data):
        """Test collecting SSD metrics."""
        mock_get_smart_data.return_value = {"Temperature_Celsius": "37"}
        metrics = collect_metrics()
        self.assertIn("/dev/sda", metrics)


if __name__ == "__main__":
    unittest.main()

