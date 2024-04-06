import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from algorithim.chart_data import check_chart_data
from unittest.mock import patch
from main import db, ExcelFile

# Purpose: if each file don't have any charts, the function should return no results for each file.
def test_check_chart_data_with_no_charts():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    chart_data = {
      1: {},
      2: {},
      3: {}
    }
    expected_result = {
      1: ([], 0),
      2: ([], 0),
      3: ([], 0)
    }
    assert check_chart_data(chart_data, db, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

# Purpose: if each file has a chart, but none of these charts reference another file within the scan list, the function should return no results.
def test_check_chart_data_with_no_cross_referencing_charts():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    chart_data = {
      1: {'File1 Chart1': {'file_name': 'file1.xlsx', 'chart_name': 'File1 Chart1', 'chart_type': '4', 'data_x_source': "'Problem 4'!$B$17:$B$36", 'data_y_source': "'Problem 4'!$C$17:$C$36", 'x_source_filename': 'Current Worksheet', 'y_source_filename': 'Current Worksheet'}},
      2: {'File2 Chart1': {'file_name': 'file2.xlsx', 'chart_name': 'File2 Chart1', 'chart_type': '4', 'data_x_source': "'Problem 3'!$A$17:$A$36", 'data_y_source': "'Problem 3'!$B$17:$B$36", 'x_source_filename': 'Current Worksheet', 'y_source_filename': 'Current Worksheet'}},
      3: {'File3 Chart1': {'file_name': 'file3.xlsx', 'chart_name': 'File3 Chart1', 'chart_type': '4', 'data_x_source': "'Problem 1'!$F$17:$G$36", 'data_y_source': "'Problem 3'!$H$17:$I$36", 'x_source_filename': 'Current Worksheet', 'y_source_filename': 'Current Worksheet'}}
    }
    expected_result = {
      1: ([], 0),
      2: ([], 0),
      3: ([], 0)
    }
    assert check_chart_data(chart_data, db, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called

# Purpose: if each file has a chart, and some of these charts reference other files within the scan list, the function should indicate which chart, which data source, and what file it references.
def test_check_chart_data_with_cross_referencing_charts():
  with patch('test_font_data.db.session') as mock_db, \
    patch('test_font_data.ExcelFile') as mock_ExcelFile:
    chart_data = {
      1: {'File1 Chart1': {'file_name': 'file1.xlsx', 'chart_name': 'File1 Chart1', 'chart_type': '4', 'data_x_source': "'[file2.xlsx]Problem 4'!$B$17:$B$36", 'data_y_source': "'[file2.xlsx]Problem 4'!$C$17:$C$36", 'x_source_filename': 'file2.xlsx', 'y_source_filename': 'file2.xlsx'}},
      2: {'File2 Chart1': {'file_name': 'file2.xlsx', 'chart_name': 'File2 Chart1', 'chart_type': '4', 'data_x_source': "'Problem 3'!$A$17:$A$36", 'data_y_source': "'Problem 3'!$B$17:$B$36", 'x_source_filename': 'Current Worksheet', 'y_source_filename': 'Current Worksheet'}},
      3: {'File3 Chart1': {'file_name': 'file3.xlsx', 'chart_name': 'File3 Chart1', 'chart_type': '4', 'data_x_source': "'[file2.xlsx]Problem 1'!$F$17:$G$36", 'data_y_source': "'Problem 3'!$H$17:$I$36", 'x_source_filename': 'file2.xlsx', 'y_source_filename': 'Current Worksheet'}}
    }
    expected_result = {
      1: (["Chart 'File1 Chart1' has a matching x source filename with file 'file2.xlsx'.", "Chart 'File1 Chart1' has a matching y source filename with file 'file2.xlsx'."], 2),
      2: ([], 0),
      3: (["Chart 'File3 Chart1' has a matching x source filename with file 'file2.xlsx'."], 1)
    }
    assert check_chart_data(chart_data, db, ExcelFile) == expected_result
    assert not mock_db.session.query.called
    assert not mock_db.session.commit.called
    assert not mock_db.session.rollback.called
    assert not mock_ExcelFile.called
