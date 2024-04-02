from main import db, ExcelFile, TemplateFile
from .fingerprint_data import check_fingerprint_data
from .column_width import check_column_width
from .author_data import check_author_data
from .font_data import check_font_data
from .chart_data import check_chart_data
from .formula_data import check_formula_data


#THIS IS A PLACEHOLDER FUNCTION THAT WILL JUST CALL AND AGGREGATE ALL THE CHECKS 
def perform_checks(scan_id):
  template_data = get_template_file_data(scan_id)
  fingerprint_data = get_fingerprint_data(scan_id)
  column_width_data = get_column_width_data(scan_id)
  author_data = get_author_data(scan_id)
  font_data = get_font_data(scan_id)
  chart_data = get_chart_data(scan_id)
  formula_data = get_formula_data(scan_id)

  # Calculate scores from each individual check
  fingerprint_files = check_fingerprint_data(fingerprint_data)
  column_width_files = check_column_width(column_width_data, template_data['column_data'] if template_data else [])
  author_data_files = check_author_data(author_data, template_data['author_data'] if template_data else [])
  font_data_files = check_font_data(font_data)
  chart_data_files = check_chart_data(chart_data)
  formula_data_files = check_formula_data(formula_data)

#   # Aggregate the scores.
#   total_score = (column_width_score + author_data_score +
#                 + font_data_score + formula_data_score) / 7  # Example averaging 

  # Return the total score
  return None

def get_fingerprint_data(scan_id):
    files = ExcelFile.query.filter_by(scan_id=scan_id).all()
    fingerprint_data = {}

    for file in files: 
      author_data = {
        "creator": file.created
      }
      formula_data = file.complex_formulas_list 

      fingerprint_data[file.file_name] = {
        'author_data': author_data, 
        'formula_data': formula_data, 
      }
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
  chart_data = None
  return chart_data

def get_formula_data(scan_id):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  formula_data = {}
  
  for file in files:
    formula_data[file.file_name] = file.complex_formulas_list
  return formula_data

#Function that will get all data from the tempate dile from db 
def get_template_file_data(scan_id):
    template_file = TemplateFile.query.filter_by(scan_id=scan_id).first()

    if template_file: 
      author_data = {
            "created": template_file.created,
            "creator": template_file.creator,
        }
      column_data = template_file.unique_column_width_list
      font_data = template_file.unique_font_names_list

      template_file_data = {
        'author_data': author_data,
        'column_data': column_data,
        'font_data': font_data,
      }
      return template_file_data
    else: 
      return None 