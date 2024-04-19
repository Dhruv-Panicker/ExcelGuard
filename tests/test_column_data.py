import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithim.column_width_data import check_column_width_data
from unittest.mock import patch
from main import db, ExcelFile

def test_column_width_no_match(): 
  with patch('test_column_data.db.session') as mock_db, \
    patch('test_column_data.ExcelFile') as mock_ExcelFile:
    file_column_data = {'file1.xlsx': [10, 20, 30]}
    template_column_data = [10, 20, 30]
    expected_result = {}
    assert check_column_width_data(file_column_data, db, ExcelFile, template_column_data) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

def test_column_width_with_match():
  with patch('test_column_data.db.session') as mock_db, \
      patch('test_column_data.ExcelFile') as mock_ExcelFile:
      file_column_data = {'file1.xlsx': [10, 23, 30], 'file2.xlsx': [10, 23, 30]}
      template_column_data = [15, 20, 35]
      expected_result = {
          'file1.xlsx': ("column_width", ["Same column width [23] as file2.xlsx"], 1),
          'file2.xlsx': ("column_width", ["Same column width [23] as file1.xlsx"], 1)
      }
      assert check_column_width_data(file_column_data, db, ExcelFile, template_column_data) == expected_result
      assert not mock_db.session.query.called
      assert not mock_db.session.commit.called
      assert not mock_db.session.rollback.called
      assert not mock_ExcelFile.called

def test_column_width_with_partial_match():
  with patch('test_column_data.db.session') as mock_db, \
      patch('test_column_data.ExcelFile') as mock_ExcelFile:
      file_column_data = {'file1.xlsx': [12, 22.64, 35.34], 'file2.xlsx': [12, 22.64, 35.34]}
      template_column_data = [12, 23.45, 30]
      expected_result = {
          'file1.xlsx': ("column_width", ["Same column width [35.34, 22.64] as file2.xlsx"], 2),
          'file2.xlsx': ("column_width", ["Same column width [35.34, 22.64] as file1.xlsx"], 2)
      }
      assert check_column_width_data(file_column_data, db, ExcelFile, template_column_data) == expected_result
      assert not mock_db.session.query.called
      assert not mock_db.session.commit.called
      assert not mock_db.session.rollback.called
      assert not mock_ExcelFile.called
