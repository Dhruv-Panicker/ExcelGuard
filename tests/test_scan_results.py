import pytest
import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from main import app, db, ExcelFile
from algorithim.plagiarism_checker import get_fingerprint_data
from algorithim.fingerprint_data import check_fingerprint_data

@pytest.fixture
def test_client():
  app.config['TESTING'] = True
  with app.test_client() as testing_client:
    with app.app_context():
      pass
    yield testing_client

def test_get_fingerprint_results():
  with app.app_context(): 
    with patch('test_scan_results.db.session') as mock_db, \
      patch('test_scan_results.ExcelFile') as mock_ExcelFile:
        scan_id = 49  # Example scan_id
        data = get_fingerprint_data(scan_id, ExcelFile)
        flagged_files = check_fingerprint_data(data, db, ExcelFile)
        assert ('fingerprint', 'matched_fingerprint_with:campbellclara_11094_313000_Assignment 1 - Clara Campbell.xlsx', 3) in flagged_files
        assert ('fingerprint', 'matched_fingerprint_with:campbellclara_Assignment_copied - Clara Campbell.xlsx', 3) in flagged_files 
        assert not mock_db.session.query.called
        assert not mock_db.session.commit.called
        assert not mock_db.session.rollback.called
        assert not mock_ExcelFile.called