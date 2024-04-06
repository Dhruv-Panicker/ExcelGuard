import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithim.font_data import check_font_data
from unittest.mock import patch
from main import db, ExcelFile
from datetime import datetime

# Purpose: if each file has an "uncommonly" used font, but none are similar, each file should have an empty list with 0 count.
def test_check_font_data_with_unique_uncommon_fonts():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    font_data = {
      1: ['Agency FB'],
      2: ['Brush Script'],
      3: ['Chalkduster', 'Lucida Calligraphy']}
    template_data = None
    expected_result = {
      1: ([], 0),
      2: ([], 0),
      3: ([], 0)}
    assert check_font_data(font_data, db, template_data, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

# Purpose: if 2 or more files have similar "uncommonly" used fonts, those files should have a list which contains the names of similar uncommon fonts with a count of how many that file has.
def test_check_font_data_with_similar_uncommon_fonts():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    font_data = {
      1: ['Agency FB'],
      2: ['Brush Script'],
      3: ['Chalkduster', 'Agency FB']}
    template_data = None
    expected_result = {
      1: (['Agency FB'], 1),
      2: ([], 0),
      3: (['Agency FB'], 1)}
    assert check_font_data(font_data, db, template_data, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

# Purpose: if 2 or more files have similar "commonly" used fonts, those files should have an empty list with 0 count.
def test_check_font_data_with_similar_common_fonts():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    font_data = {
      1: ['Calibri'],
      2: ['Calibri', 'Palatino Linotype'],
      3: ['Palatino Linotype', 'Calibri Light']}
    template_data = None
    expected_result = {
      1: ([], 0),
      2: ([], 0),
      3: ([], 0)}
    assert check_font_data(font_data, db, template_data, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

# Purpose: if 2 or more files have similar "uncommonly" used fonts, but those same fonts are also found in the provided template file, those files should have an empty list with 0 count.
def test_check_font_data_with_similar_uncommon_fonts_in_template_file():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    font_data = {
      1: ['Agency FB'],
      2: ['Brush Script'],
      3: ['Chalkduster', 'Agency FB']}
    template_data = {
      'author_data': {'created': datetime.now(), 'creator': 'UserA'},
      'column_data': [34.36328125, 11.54296875, 13.0, 176.1796875, 49.08984375, 17.1796875, 20.0, 59.1796875],
      'font_data': ['Agency FB']}
    expected_result = {
      1: ([], 0),
      2: ([], 0),
      3: ([], 0)}
    assert check_font_data(font_data, db, template_data, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called
