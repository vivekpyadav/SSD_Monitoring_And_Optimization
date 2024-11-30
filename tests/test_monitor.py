import unittest
import sys
sys.path.append("/home/kalilinux_user/devops/SSD_project")
from src.monitor import parse_smart_data


class TestMonitor(unittest.TestCase):
    def test_parse_smart_data_valid(self):
        """Test parsing valid SMART data output."""
        smart_output = """
        ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
        1   Raw_Read_Error_Rate     0x000f   100   100   006    Pre-fail  Always       -       0
        5   Reallocated_Sector_Ct   0x0033   100   100   036    Pre-fail  Always       -       0
        194 Temperature_Celsius     0x0022   037   062   000    Old_age   Always       -       37
        """
        expected = {
            "Raw_Read_Error_Rate": "0",
            "Reallocated_Sector_Ct": "0",
            "Temperature_Celsius": "37",
        }
        self.assertEqual(parse_smart_data(smart_output), expected)

    def test_parse_smart_data_invalid(self):
        """Test parsing invalid SMART data output."""
        smart_output = "Invalid data format"
        self.assertEqual(parse_smart_data(smart_output), {})


if __name__ == "__main__":
    unittest.main()

