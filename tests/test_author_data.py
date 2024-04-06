import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from algorithim.author_data import check_author_data

def test_author_data_no_duplicates():
  author_data = {
    'file1.xlsx': {
      'creator': 'userA', 
      'created': datetime(2022, 1, 1),
      'lastModifiedBy': datetime(2022, 1, 2)
    }
  }
  template_author_data = {
    'creator': 'professor', 
    'created': datetime(2021, 12, 31),
    'lastModifiedBy': datetime(2021, 12, 31)
  }
  expected_result = {}
  assert check_author_data(author_data, template_author_data) == expected_result

def test_author_data_with_duplicates():
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
    'created': datetime(2021, 12, 31),
    'lastModifiedBy': datetime(2021, 12, 31)
  }
  expected_result = {
    'file1.xlsx': ['same_creator:userA'],
    'file2.xlsx': ['same_creator:userA']}
  assert check_author_data(author_data, template_author_data) == expected_result

def test_author_data_with_same_creation_date():
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
    'created': datetime(2021, 12, 31),
    'lastModifiedBy': datetime(2021, 12, 31)
  }
  expected_result = {
    'file1.xlsx': ['same_creation_date:2022-01-01 00:00:00'],
    'file2.xlsx': ['same_creation_date:2022-01-01 00:00:00']}
  assert check_author_data(author_data, template_author_data) == expected_result
