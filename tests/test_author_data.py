import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from algorithim.author_data import check_author_data
from unittest.mock import patch
from main import db, ExcelFile


def test_author_data_no_duplicates():
  with patch('test_author_data.db.session') as mock_db, \
    patch('test_author_data.ExcelFile') as mock_ExcelFile:
    author_data = {
      'file1.xlsx': {
        'creator': 'userA', 
        'created': datetime(2022, 1, 1),
        'lastModifiedBy': datetime(2022, 1, 2)
      }
    }
    template_author_data = {
      'creator': 'professor', 
      'created': datetime(2021, 12, 31)
    }
    expected_result = {}
    assert check_author_data(author_data, db, ExcelFile, template_author_data) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

def test_author_data_with_duplicates():
  with patch('test_author_data.db.session') as mock_db, \
    patch('test_author_data.ExcelFile') as mock_ExcelFile:
    author_data = {
      'file1.xlsx': {
        'creator': 'userA', 
        'created': datetime(2022, 1, 1),
        'lastModifiedBy': datetime(2022, 1, 2)
      },
      'file2.xlsx': {
        'creator': 'userA', 
        'created': datetime(2022, 1, 3),
        'lastModifiedBy': datetime(2022, 1, 4)
      }
    }
    template_author_data = {
      'creator': 'professor', 
      'created': datetime(2021, 12, 31)
    }
    expected_result = {
      'file1.xlsx': [("author_data", 'Same creator:userA as file2.xlsx', 3)],
      'file2.xlsx': [("author_data", 'Same creator:userA as file1.xlsx', 3)]
    }
    assert check_author_data(author_data, db, ExcelFile, template_author_data) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called


def test_author_data_with_same_creation_date():
  with patch('test_author_data.db.session') as mock_db, \
    patch('test_author_data.ExcelFile') as mock_ExcelFile:
    author_data = {
      'file1.xlsx': {
        'creator': 'userA', 
        'created': datetime(2022, 1, 1),
        'lastModifiedBy': datetime(2022, 1, 2)
      },
      'file2.xlsx': {
        'creator': 'userB', 
        'created': datetime(2022, 1, 1),
        'lastModifiedBy': datetime(2022, 1, 3)
      }
    }
    template_author_data = {
      'creator': 'professor', 
      'created': datetime(2021, 12, 31)
    }
    expected_result = {
      'file1.xlsx': [("author_data", 'Same creation date:01/01/2022 as file2.xlsx', 2)],
      'file2.xlsx': [("author_data", 'Same creation date:01/01/2022 as file1.xlsx', 2)]
    }
    assert check_author_data(author_data, db, ExcelFile, template_author_data) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called
