import unittest
from unittest.mock import patch
import sys
sys.path.append("/home/kalilinux_user/devops/SSD_project")
from src.maintenance import run_trim


class TestMaintenance(unittest.TestCase):
    @patch("subprocess.run")
    def test_run_trim_success(self, mock_run):
        """Test successful execution of TRIM."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "TRIM completed successfully"
        run_trim("/dev/sda")
        mock_run.assert_called_with(["sudo","fstrim", "/dev/sda"], stdout=-1, stderr=-1, text=True)

    @patch("subprocess.run")
    def test_run_trim_failure(self, mock_run):
        """Test failure of TRIM command."""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Error: TRIM not supported"
        run_trim("/dev/sda")
        mock_run.assert_called_with(["sudo","fstrim", "/dev/sda"], stdout=-1, stderr=-1, text=True)


if __name__ == "__main__":
    unittest.main()

