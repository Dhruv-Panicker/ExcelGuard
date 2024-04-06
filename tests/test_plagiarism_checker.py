import pytest
import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app, ExcelFile, ExcelChart
from algorithim.plagiarism_checker import get_fingerprint_data, get_column_width_data, get_author_data, get_font_data, get_formula_data, get_chart_data

@pytest.fixture
def test_client():
  app.config['TESTING'] = True
  with app.test_client() as testing_client:
    with app.app_context():
      pass
    yield testing_client

def test_get_fingerprint_data(test_client):
  with app.app_context(): 
    scan_id = 56  # Example scan_id
    data = get_fingerprint_data(scan_id, ExcelFile)
    assert isinstance(data, dict)  # Ensure it returns a dictionary
    print("Fingerprint Data:", data)

def test_get_column_width_data(test_client):
  with app.app_context(): 
    scan_id = 56  # Example scan_id
    data = get_column_width_data(scan_id, ExcelFile)
    assert isinstance(data, dict)  # Ensure it returns a dictionary
    print("Column Width Data:", data)

def test_get_author_data(test_client):
  with app.app_context(): 
    scan_id = 56  # Example scan_id
    data = get_author_data(scan_id, ExcelFile)
    assert isinstance(data, dict)  # Ensure it returns a dictionary
    print("Author Data:", data)

def test_get_font_data(test_client):
  with app.app_context(): 
    scan_id = 56  # Example scan_id
    data = get_font_data(scan_id, ExcelFile)
    assert isinstance(data, dict)  # Ensure it returns a dictionary
    print("Font Data:", data)

def test_get_formula_data(test_client):
  with app.app_context(): 
    scan_id = 56  # Example scan_id
    data = get_formula_data(scan_id, ExcelFile)
    assert isinstance(data, dict)  # Ensure it returns a dictionary
    print("Formula Data:", data)
        
def test_get_chart_data(test_client):
  with app.app_context(): 
    scan_id = 56  # Example scan_id
    data = get_chart_data(scan_id, ExcelFile, ExcelChart)
    assert isinstance(data, dict)  # Ensure it returns a dictionary
    print("Formula Data:", data)

if __name__ == "__main__":
  pytest.main()