import re
from .fingerprint_data import check_fingerprint_data
from .column_width import check_column_width
from .author_data import check_author_data
from .font_data import check_font_data
from .chart_data import check_chart_data
from .formula_data import check_formula_data

DEFAULT_SERIES_FILE_DATA_SOURCE = "Current Worksheet"
FORMULA_INSIDE_BRACKETS = r'\(([^)]+)\)'
FORMULA_INSIDE_SQUARE_BRACKETS = r'\[([^\]]+)\]'

def perform_checks(scan_id, db, ExcelFile, ExcelChart, TemplateFile):
  template_data = get_template_file_data(scan_id, TemplateFile)
  # fingerprint_data = get_fingerprint_data(scan_id, ExcelFile)
  # column_width_data = get_column_width_data(scan_id, ExcelFile)
  author_data = get_author_data(scan_id, ExcelFile)
  font_data = get_font_data(scan_id, ExcelFile)
  chart_data = get_chart_data(scan_id, ExcelFile, ExcelChart)
  # formula_data = get_formula_data(scan_id, ExcelFile)

  # Calculate scores from each individual check
  chart_data_scores = 0
  # fingerprint_score = check_fingerprint_data(fingerprint_data)
  # column_width_files = check_column_width(column_width_data, template_data["column_data"] if template_data else [])
  author_data_files = check_author_data(author_data, db, ExcelFile, template_data["author_data"] if template_data else None)
  font_component_score = check_font_data(font_data, db, template_data, ExcelFile)
  chart_component_score = check_chart_data(chart_data, db, ExcelFile)
  # formula_data_score = check_formula_data(formula_data)


  # Aggregate the scores.
  # total_score = (column_width_score + author_data_score +
  #               + font_data_score + formula_data_score) / 7  # Example averaging 

  # Return the total score
  return chart_component_score

def get_fingerprint_data(scan_id, ExcelFile):
    files = ExcelFile.query.filter_by(scan_id=scan_id).all()
    fingerprint_data = {}

    for file in files: 
      author_data = {
        "creator": file.created
      }
      formula_data = file.complex_formulas_list 

      fingerprint_data[file.id] = {
        "author_data": author_data, 
        "formula_data": formula_data, 
      }
    return fingerprint_data


def get_column_width_data(scan_id, ExcelFile):
  # Query all excel_files which have the scan_id
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  column_width_data = {}

  for file in files:
    unique_column_width_list = file.unique_column_width_list
    
    # Add the file name and its unique column width list to the column_data dictionary
    column_width_data[file.id] = unique_column_width_list
  return column_width_data

def get_author_data(scan_id, ExcelFile):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  author_data = {}
  
  for file in files:
    author_data[file.id] = {
      "created": file.created,
      "creator": file.creator,
      "modified": file.modified,
      "lastModifiedBy": file.last_modified_by
      }
  return author_data

def get_font_data(scan_id, ExcelFile):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  font_data = {}
  
  for file in files:
    font_data[file.id] = file.unique_font_names_list
  return font_data

def get_chart_data(scan_id, ExcelFile, ExcelChart):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  chart_data = {}
  for file in files:
    # Get theExcelCharts for the current ExcelFile
    charts = ExcelChart.query.filter_by(excel_file_id=file.id).all()
  
    # Store chart data for the current ExcelFile
    chart_data[file.id] = {}
  
    for chart in charts:
      data_source_str = chart.data_source
      data_x_source = ""
      data_y_source = ""
      x_source_filename = DEFAULT_SERIES_FILE_DATA_SOURCE
      y_source_filename = DEFAULT_SERIES_FILE_DATA_SOURCE
      regular_expression_match = re.findall(FORMULA_INSIDE_BRACKETS, data_source_str)

      # The Series information should have 4 elements, a title, x data values, y data values, and series plot type
      if regular_expression_match:
        regular_expression_match_elements = regular_expression_match[0].split(',')
        data_x_source = regular_expression_match_elements[1]
        data_y_source = regular_expression_match_elements[2]

      x_data_source_match = re.findall(FORMULA_INSIDE_SQUARE_BRACKETS, data_x_source)
      if x_data_source_match:
        x_source_filename = x_data_source_match[0]
      
      y_data_source_match = re.findall(FORMULA_INSIDE_SQUARE_BRACKETS, data_y_source)
      if x_data_source_match:
        y_source_filename = y_data_source_match[0]

      chart_info = {
        "chart_name": chart.chart_name,
        "chart_type": chart.chart_type,
        "data_x_source": data_x_source,
        "data_y_source": data_y_source,
        "x_source_filename": x_source_filename,
        "y_source_filename": y_source_filename
      }
      chart_data[file.id][chart.chart_name] = chart_info
  return chart_data

def get_formula_data(scan_id, ExcelFile):
  files = ExcelFile.query.filter_by(scan_id=scan_id).all()
  formula_data = {}
  
  for file in files:
    formula_data[file.id] = file.complex_formulas_list
  return formula_data

# Function that will get all data from the template file from db 
def get_template_file_data(scan_id, TemplateFile):
    template_file = TemplateFile.query.filter_by(scan_id=scan_id).first()

    if template_file: 
      author_data = {
        "created": template_file.created,
        "creator": template_file.creator,
        }
      column_data = template_file.unique_column_width_list
      font_data = template_file.unique_font_names_list

      template_file_data = {
        "author_data": author_data,
        "column_data": column_data,
        "font_data": font_data,
      }
      return template_file_data
    else: 
      return None 
