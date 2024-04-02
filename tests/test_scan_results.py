import pytest
import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, db
from algorithim.plagiarism_checker import get_fingerprint_data
from algorithim.fingerprint_data import generate_fingerprint, check_fingerprint_data

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.test_client() as testing_client:
        with app.app_context():
            pass
        yield testing_client

def test_get_fingerprint_results(test_client):
    with app.app_context(): 
        scan_id = 58  # Example scan_id
        data = get_fingerprint_data(scan_id)
        flagged_files = check_fingerprint_data(data)
        assert ('campbellclara_Assignment_copied - Clara Campbell.xlsx', 'matched_fingerprint_with:campbellclara_11094_313000_Assignment 1 - Clara Campbell.xlsx') in flagged_files
        assert ('campbellclara_11094_313000_Assignment 1 - Clara Campbell.xlsx', 'matched_fingerprint_with:campbellclara_Assignment_copied - Clara Campbell.xlsx') in flagged_files 
        print("Fingerprint Data:", flagged_files)