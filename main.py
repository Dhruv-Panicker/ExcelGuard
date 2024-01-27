from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles.fonts import Font



app = Flask(__name__)
Bootstrap(app)
@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/scan_list")
def scan_list(): 
  return render_template("scan_list.html")

@app.route("/begin_scan", methods=['POST'])
def begin_scan():
  template_file = None
  # If TemplateFile is uploaded assign it to our templateFile variable to it
  if "templateFile" in request.files:
    if request.files["templateFile"].filename != "":
      template_file = request.files["templateFile"]
  # Assign uploaded assignment files to assignmentFiles variable
  assignment_files = request.files.getlist("assignmentFiles")
  # Saving the uploaded files so that they can be accessed
  if template_file is not None:
    if template_file:
      try:
        # Set the directory and file path where the template file will be saved and save it
        template_files_folder = "scan_template_uploads"
        os.makedirs(template_files_folder, exist_ok=True)
        template_file_path = os.path.join(template_files_folder, file.filename)
        file.save(template_file_path)
      except Exception as e:
        return f"Error processing the file: {str(e)}"
  for file in assignment_files:
    if file:
      try:
        # Set the directory and file path where the assignment file will be saved and save it
        assignment_files_folder = "scan_assignment_uploads"
        os.makedirs(assignment_files_folder, exist_ok=True)
        assignment_file_path = os.path.join(assignment_files_folder, file.filename)
        file.save(assignment_file_path)
        author_data_list = get_author_data(assignment_files)
      except Exception as e:
        return f"Error processing the file: {str(e)}"
    print(f"{author_data_list}")
  return "Done"

@app.route("/scanning")
def scanning():
  return render_template("scanning.html")

@app.route("/scan_results")
def scan_results():
  return render_template("scan_results.html")

@app.route("/view_scan")
def view_scan():
  return render_template("view_scan.html")

@app.route("/settings")
def settings():
  return render_template("settings.html")

@app.route("/logout")
def logout():
  return render_template("logout.html")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)

def column_data(excel_files):
  column_data_list = []
  # Go through each file in the given list of excel files
  for file in excel_files:
    try:
      # If the file has no filename, something went wrong
      if file.filename == "":
        print(f"Could not retrieve filename from {file}")
      # Otherwise save the file, open the workbook, go through each sheet and store the unique column widths (in each respective sheet)
      else:
        if file:
          file_widths = set()
          assignment_files_folder = "scan_assignment_uploads"
          assignment_file_path = os.path.join(assignment_files_folder, file.filename)
          excel_workbook = load_workbook(assignment_file_path)
          for sheet_name in excel_workbook.sheetnames:
            excel_sheet = excel_workbook[sheet_name]
            for column in excel_sheet.columns:
              width = excel_sheet.column_dimensions[column[0].column_letter].width
              file_widths.append(width)
      column_data_list.add(file_widths)
    except Exception as e:
      print(f"Error reading {file}: {str(e)}")
  return column_data_list

def get_author_data(excel_files):
  author_data_list = []
  # Go through each file in the given list of excel files
  for file in excel_files:
    try:
      # If the file has no filename, something went wrong
      if file.filename == "":
        print(f"Could not retrieve filename from {file}")
      else:
        # Otherwise save the file, open the workbook, and store the workbook properties (contains file metadata like creator, title, description, createdDate, lastModifiedDate, lastModifiedBy, etc)
        if file: 
          assignment_files_folder = "scan_assignment_uploads"
          assignment_file_path = os.path.join(assignment_files_folder, file.filename)
          excel_workbook = load_workbook(assignment_file_path)
          author_data_list.append(excel_workbook.properties).tolist()
    except Exception as e:
      print(f"Error reading {file}: {str(e)}")
  return author_data_list

def get_shape_data(excel_files):
  shape_data_list = []
  return shape_data_list

def get_font_names(excel_files):
  font_names_list = []
  # Go through each file in the given list of excel files
  for file in excel_files:
    try:
      # If the file has no filename, something went wrong
      if file.filename == "":
        print(f"Could not retrieve filename from {file}")
      else:
        # Otherwise save the file, open the workbook, and get every unique font from each file and store them into a list (which contains all the unique fonts used by each excel file)
        if file:
          file_font_names = set()
          assignment_files_folder = "scan_assignment_uploads"
          assignment_file_path = os.path.join(assignment_files_folder, file.filename)
          excel_workbook = load_workbook(assignment_file_path)
          for sheet_name in excel_workbook.sheetnames:
            excel_sheet = excel_workbook[sheet_name]
            for row in excel_sheet.iter_rows(min_row=1, max_col=excel_sheet.max_column, max_row=excel_sheet.max_row):
              for cell in row:
                font = cell.font
                if font.name not in file_font_names: 
                  file_font_names.add(font.name)
      font_names_list.append(file_font_names)
    except Exception as e:
      print(f"Error reading {file}: {str(e)}")
  return font_names_list

def get_link_data(excel_files):
  link_data_list = []
  return link_data_list

def get_formula_data(excel_files):
  formula_data_list = []
  return formula_data_list
