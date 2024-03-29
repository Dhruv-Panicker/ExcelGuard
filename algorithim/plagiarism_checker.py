from main import db, ExcelFile
from .fingerprint_data import check_fingerprint_data
from .column_data import check_column_data
from .author_data import check_author_data
from .font_data import check_font_data
from .chart_data import check_chart_data
from .formula_data import check_formula_data

# algorithm/plagiarism_checker.py
#Function that will get all data from the beign_scan function 
def get_file_data(author_data, column_data, font_data, formula_data, chart_data):
    file_data = {
        'author_data': author_data,
        'column_data': column_data,
        'font_data': font_data,
        'formula_data': formula_data,
        'chart_data': chart_data
    }
    return file_data

def get_template_file_data(author_data, column_data, font_data, formula_data, chart_data):
    template_file_data = {
        'author_data': author_data,
        'column_data': column_data,
        'font_data': font_data,
        'formula_data': formula_data,
        'chart_data': chart_data
    }
    return template_file_data


#THIS IS A PLACEHOLDER FUNCTION THAT WILL JUST CALL AND AGGREGATE ALL THE CHECKS 
def perform_checks(scan_id):
  fingerprint_data = get_fingerprint_data(scan_id)
  column_width_data = get_column_width_data(scan_id)
  author_data = get_author_data(scan_id)
  font_data = get_font_data(scan_id)
  chart_data = get_chart_data(scan_id)
  formula_data = get_formula_data(scan_id)

  # Calculate scores from each individual check
  fingerprint_score = check_fingerprint_data(fingerprint_data)
  column_width_score = check_column_data(column_width_data)
  author_data_score = check_author_data(author_data)
  font_data_score = check_font_data(font_data)
  chart_data_score = check_chart_data(chart_data)
  formula_data_score = check_formula_data(formula_data)

  # Aggregate the scores.
  total_score = (column_width_score + author_data_score +
                + font_data_score + formula_data_score) / 7  # Example averaging 

  # Return the total score
  return total_score

def get_fingerprint_data(scan_id):
  #TODO
  return fingerprint_data 

def get_column_width_data(scan_id):
  # Query all excel_files which have the scan_id
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  column_width_data = {}

  for file in files:
    # Extract file name and unique column width list
    file_name = file.file_name
    unique_column_width_list = file.unique_column_width_list
    
    # Add the file name and its unique column width list to the column_data dictionary
    column_width_data[file_name] = unique_column_width_list
  return column_width_data

def get_author_data(scan_id):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  author_data = {}
  
  for file in files:
    author_data[file.file_name] = {
      "created": file.created,
      "creator": file.creator,
      "modified": file.modified,
      "lastModifiedBy": file.last_modified_by
      }
  return author_data

def get_font_data(scan_id):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  font_data = {}
  
  for file in files:
    font_data[file.file_name] = file.unique_font_names_list
  return font_data

def get_chart_data(scan_id):
  #TODO
  return chart_data

def get_formula_data(scan_id):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  formula_data = {}
  
  for file in files:
    formula_data[file.file_name] = file.complex_formulas_list
  return formula_data
