import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithim.column_width import check_column_width

def test_column_width_no_match():
    file_column_data = {'file1.xlsx': [10, 20, 30]}
    template_column_data = [10, 20, 30]
    assert check_column_width(file_column_data, template_column_data) == []

def test_column_width_with_match():
    file_column_data = {'file1.xlsx': [10, 20, 30], 'file2.xlsx': [10, 20, 30]}
    template_column_data = [15, 25, 35]
    assert check_column_width(file_column_data, template_column_data) == [('file1.xlsx', [10, 20, 30]), ('file2.xlsx', [10, 20, 30])]

def test_column_width_with_partial_match():
    file_column_data = {'file1.xlsx': [10, 20, 35], 'file2.xlsx': [12, 20, 35]}
    template_column_data = [10, 20, 30]
    assert check_column_width(file_column_data, template_column_data) == [('file1.xlsx', [35]), ('file2.xlsx', [35])]