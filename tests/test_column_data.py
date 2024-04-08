import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithim.column_width import check_column_width
from unittest.mock import patch
from main import db, ExcelFile

def test_column_width_no_match(): 
    with patch('test_column_data.db.session') as mock_db, \
      patch('test_column_data.ExcelFile') as mock_ExcelFile:
      file_column_data = {'file1.xlsx': [10, 20, 30]}
      template_column_data = [10, 20, 30]
      expected_result = {}
      assert check_column_width(file_column_data, db, ExcelFile, template_column_data) == expected_result
      assert not mock_db.session.query.called
      assert not mock_db.session.commit.called
      assert not mock_db.session.rollback.called
      assert not mock_ExcelFile.called

def test_column_width_with_match():
    with patch('test_column_data.db.session') as mock_db, \
       patch('test_column_data.ExcelFile') as mock_ExcelFile:
        file_column_data = {'file1.xlsx': [10, 20, 30], 'file2.xlsx': [10, 20, 30]}
        template_column_data = [15, 25, 35]
        expected_result = {
            'file1.xlsx': ("column_width", [10, 20, 30], 3),
            'file2.xlsx': ("column_width", [10, 20, 30], 3)
        }
        assert check_column_width(file_column_data, db, ExcelFile, template_column_data) == expected_result
        assert not mock_db.session.query.called
        assert not mock_db.session.commit.called
        assert not mock_db.session.rollback.called
        assert not mock_ExcelFile.called


def test_column_width_with_partial_match():
    with patch('test_column_data.db.session') as mock_db, \
       patch('test_column_data.ExcelFile') as mock_ExcelFile:
        file_column_data = {'file1.xlsx': [10, 20, 35], 'file2.xlsx': [12, 20, 35]}
        template_column_data = [10, 20, 30]
        expected_result = {
            'file1.xlsx': ("column_width", [35], 1),
            'file2.xlsx': ("column_width", [35], 1)
        }
        assert check_column_width(file_column_data, db, ExcelFile, template_column_data) == expected_result
        assert not mock_db.session.query.called
        assert not mock_db.session.commit.called
        assert not mock_db.session.rollback.called
        assert not mock_ExcelFile.called
