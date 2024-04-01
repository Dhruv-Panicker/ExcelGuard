import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithim.author_data import check_author_data

def test_author_data_no_duplicates():
    author_data = {'file1.xlsx': {'creator': 'userA', 'created': 'date1'}}
    template_author_data = {'creator': 'professor', 'created': 'date0'}
    assert check_author_data(author_data, template_author_data) == []

def test_author_data_with_duplicates():
    author_data = {
        'file1.xlsx': {'creator': 'userA', 'created': 'date1'},
        'file2.xlsx': {'creator': 'userA', 'created': 'date2'},
    }
    template_author_data = {'creator': 'professor', 'created': 'date0'}
    assert check_author_data(author_data, template_author_data) == [('file1.xlsx', 'same_creator:userA'), ('file2.xlsx', 'same_creator:userA')]

def test_author_data_with_same_creation_date():
    author_data = {
        'file1.xlsx': {'creator': 'userA', 'created': 'date1'},
        'file2.xlsx': {'creator': 'userB', 'created': 'date1'},
    }
    template_author_data = {'creator': 'professor', 'created': 'date0'}
    assert check_author_data(author_data, template_author_data) == [('file1.xlsx', 'same_creation_date:date1'), ('file2.xlsx', 'same_creation_date:date1')]
