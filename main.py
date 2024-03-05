from flask import Flask, request, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import os
from openpyxl import load_workbook
import psycopg2
from datetime import datetime
from typing import List

app = Flask(__name__)
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = {
    'postgresql': 'postgresql://tzvupyse:uiTK_Ha5MwII2BTsuCVyIA749Ut8e4Y0@baasu.db.elephantsql.com/tzvupyse',
}
connection = psycopg2.connect('postgresql://tzvupyse:uiTK_Ha5MwII2BTsuCVyIA749Ut8e4Y0@baasu.db.elephantsql.com/tzvupyse')
cursor = connection.cursor()
app.config["SECRET_KEY"] = "thisisasecretkey"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(db.Model, UserMixin): 
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  password = db.Column(db.String(80), nullable=False)

class RegistrationForm(FlaskForm): 
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
  password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Register")

  def validate_username(self, username): 
    existing_user_username = User.query.filter_by(username=username.data).first()

    if existing_user_username: 
      raise ValidationError("This username already exists. PLease choose another one.")

class LoginForm(FlaskForm): 
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
  password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
  submit = SubmitField("Login")
  
# PostgreSQL database models 
class PostgreSQLUser(db.Model):
  __bind_key__ = 'postgresql'
  __tablename__ = 'postgresql_users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)

class Scan(db.Model):
  __bind_key__ = 'postgresql'
  id = db.Column(db.Integer, primary_key=True)
  assignment_name = db.Column(db.String(255))
  course_name = db.Column(db.String(255))
  date_created = db.Column(db.TIMESTAMP, default=datetime.utcnow)
  number_of_files = db.Column(db.Integer)
  number_of_flagged_files = db.Column(db.Integer)
  user_created_by = db.Column(db.String(255))
  children: Mapped[List["ExcelFile"]] = relationship()
  children: Mapped[List["TemplateFile"]] = relationship()
  __tablename__ = "scans"

class ExcelFile(db.Model):
  __bind_key__ = 'postgresql'
  id = db.Column(db.Integer, primary_key=True)
  scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))
  file_name = db.Column(db.String(255))
  created = db.Column(db.TIMESTAMP)
  creator = db.Column(db.String(255))
  modified = db.Column(db.TIMESTAMP)
  last_modified_by = db.Column(db.String(255))
  submitted_date =db.Column(db.TIMESTAMP)
  plagiarism_percentage = db.Column(db.Integer)
  unique_column_width_list = db.Column(ARRAY(db.Integer))
  unique_font_names_list = db.Column(ARRAY(db.String(255)))
  complex_formulas_list =db.Column(ARRAY(db.String(255)))
  children: Mapped[List["ExcelShape"]] = relationship()
  children: Mapped[List["ExcelChart"]] = relationship()
  __tablename__ = "excel_files"
  
class TemplateFile(db.Model):
  __bind_key__ = 'postgresql'
  id = db.Column(db.Integer, primary_key=True)
  scan_id: Mapped[int] = mapped_column(ForeignKey("scans.id"))
  file_name = db.Column(db.String(255))
  creator = db.Column(db.String(255))
  unique_column_width_list = db.Column(ARRAY(db.Integer))
  unique_font_names_list = db.Column(ARRAY(db.String(255)))
  __tablename__ = "template_files"
  
class ExcelShape(db.Model):
  __bind_key__ = 'postgresql'
  id = db.Column(db.Integer, primary_key=True)
  excel_file_id: Mapped[int] = mapped_column(ForeignKey("excel_files.id"))
  shape_type = db.Column(db.String(255))
  shape_left = db.Column(db.Integer)
  shape_top = db.Column(db.Integer)
  shape_width = db.Column(db.Integer)
  shape_height = db.Column(db.Integer)
  __tablename__ = "excel_shapes"
  
class ExcelChart(db.Model):
  __bind_key__ = 'postgresql'
  id = db.Column(db.Integer, primary_key=True)
  excel_file_id: Mapped[int] = mapped_column(ForeignKey("excel_files.id"))
  data_source = db.Column(db.String(255))
  chart_type = db.Column(db.String(255))
  chart_left = db.Column(db.Integer)
  chart_top = db.Column(db.Integer)
  chart_width = db.Column(db.Integer)
  chart_height = db.Column(db.Integer)
  __tablename__ = "excel_charts"


# Create the databases and tables
with app.app_context():
  db.create_all()
  # cursor.execute("CREATE TABLE scans(id SERIAL PRIMARY KEY, assignment_name VARCHAR(255) NOT NULL, course_name VARCHAR(255) NOT NULL, date_created TIMESTAMP NOT NULL, number_of_files INTEGER, number_of_flagged_files INTEGER, user_created_by VARCHAR(255) NOT NULL)")

@app.route("/login", methods=["GET", "POST"])
def login(): 
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user: 
      if bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user)
        return redirect(url_for("scan_list"))
  return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
  logout_user()
  return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
  form = RegistrationForm()

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    new_user = User(username=form.username.data, password=hashed_password)

    db.session.add(new_user)
    try:
      db.session.commit()
      print("User added successfully")  # Debugging message
    except Exception as e:
      print("Failed to add user:", e) 
      return redirect(url_for("login"))
  else:
    print("Form not validated")  # Debugging message
    print(form.errors)         
  print("Database file path:", os.path.join(os.getcwd(), "database.db"))
  return render_template("register.html", form=form)

@app.route("/scan_list")
@login_required
def scan_list(): 
  PREVIOUS_SCANS_LIST_LIMIT = 5
  cursor.execute("SELECT * FROM scans")
  previous_scans_list = cursor.fetchmany(PREVIOUS_SCANS_LIST_LIMIT)
  return render_template("scan_list.html", previous_scans=previous_scans_list)

@app.route("/begin_scan", methods=["POST"])
@login_required
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
  author_data_list = {}
  column_data_list = {}
  font_data_list = {}
  formula_data_list = {}
  new_scan = Scan(assignment_name=request.form.get('assignmentName'), course_name=request.form.get('courseCode'), date_created=datetime.now(), number_of_files=len(assignment_files), user_created_by="Pirana")
  db.session.add(new_scan)
  db.session.commit()
  for file in assignment_files:
    if file:
      try:
        # Set the directory and file path where the assignment file will be saved and save it
        assignment_files_folder = "scan_assignment_uploads"
        os.makedirs(assignment_files_folder, exist_ok=True)
        assignment_file_path = os.path.join(assignment_files_folder, file.filename)
        file.save(assignment_file_path)
        
        author_data_list[file.filename] = get_author_data(file)
        column_data_list[file.filename] = get_column_data(file)
        font_data_list[file.filename] = get_font_names(file)
        formula_data_list[file.filename] = get_formula_data(file)
      except Exception as e:
        return f"Error processing the file: {str(e)}"
  return render_template("scanning.html", author_data=author_data_list, column_data=column_data_list, font_data=font_data_list, formula_data=formula_data_list)

@app.route("/scanning")
@login_required
def scanning():
  return render_template("scanning.html")

@app.route("/scan_results")
@login_required
def scan_results():
  return render_template("scan_results.html")

@app.route("/view_scan")
@login_required
def view_scan():
  return render_template("view_scan.html")

@app.route("/settings")
@login_required
def settings():
  return render_template("settings.html")

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

if __name__ == "__main__":
  app.run(host="127.0.0.1", Pport=8080, debug=True)

def get_column_data(excel_file):
  file_widths = set()
  # Go through each file in the given list of excel files
  try:
    # If the file has no filename, something went wrong
    if excel_file.filename == "":
      print(f"Could not retrieve filename from {excel_file}")
    # Otherwise save the file, open the workbook, go through each sheet and store the unique column widths (in each respective sheet)
    else:
      if excel_file:
        assignment_files_folder = "scan_assignment_uploads"
        assignment_file_path = os.path.join(assignment_files_folder, excel_file.filename)
        excel_workbook = load_workbook(assignment_file_path)
        for sheet_name in excel_workbook.sheetnames:
          excel_sheet = excel_workbook[sheet_name]
          for column in excel_sheet.columns:
            width = excel_sheet.column_dimensions[column[0].column_letter].width
            file_widths.add(width)
  except Exception as e:
    print(f"Error reading {excel_file}: {str(e)}")
  return file_widths

def get_author_data(excel_file):
  file_author_list = {}
  try:
    # If the file has no filename, something went wrong
    if excel_file.filename == "":
      print(f"Could not retrieve filename from {excel_file}")
    else:
      # Otherwise save the file, open the workbook, and store the workbook properties (contains file metadata like creator, title, description, createdDate, lastModifiedDate, lastModifiedBy, etc)
      if excel_file: 
        assignment_files_folder = "scan_assignment_uploads"
        assignment_file_path = os.path.join(assignment_files_folder, excel_file.filename)
        excel_workbook = load_workbook(assignment_file_path)
        file_author_list["creator"] = excel_workbook.properties.creator
        file_author_list["created"] = excel_workbook.properties.created
        file_author_list["modified"] = excel_workbook.properties.modified
        file_author_list["lastModifiedBy"] = excel_workbook.properties.lastModifiedBy
  except Exception as e:
    print(f"Error reading {excel_file}: {str(e)}")
  return file_author_list

#TODO
def get_shape_data(excel_files):
  # shape_data_list = []
  #   # Go through each file in the given list of excel files
  # for file in excel_files:
  #   try:
  #     # If the file has no filename, something went wrong
  #     if file.filename == "":
  #       print(f"Could not retrieve filename from {file}")
  #     else:
  #       # Otherwise save the file, open the workbook, and get the formula from every cell which contains a formula
  #       if file:
  #         file_shape_list = []
  #         assignment_files_folder = "scan_assignment_uploads"
  #         assignment_file_path = os.path.join(assignment_files_folder, file.filename)
  #         excel_workbook = load_workbook(assignment_file_path)
  #         for sheet in excel_workbook:
  #           for shape_id, shape in sheet.shapes.items():
  #             shape_type = shape.type
  #             left = shape.left
  #             top = shape.top
  #             width = shape.width
  #             height = shape.height
  #             file_shape_list.append({
  #               "Shape ID": shape_id,
  #               "Type": shape_type,
  #               "Left": left,
  #               "Top": top,
  #               "Width": width,
  #               "Height": height,
  #           })
  #   except Exception as e:
  #     print(f"Error reading {file}: {str(e)}")
  return shape_data_list

def get_font_names(excel_file):
  font_names_list = []
  try:
    # If the file has no filename, something went wrong
    if excel_file.filename == "":
      print(f"Could not retrieve filename from {excel_file}")
    else:
      # Otherwise save the file, open the workbook, and get every unique font from each file and store them into a list (which contains all the unique fonts used by each excel file)
      if excel_file:
        assignment_files_folder = "scan_assignment_uploads"
        assignment_file_path = os.path.join(assignment_files_folder, excel_file.filename)
        excel_workbook = load_workbook(assignment_file_path)
        for sheet_name in excel_workbook.sheetnames:
          excel_sheet = excel_workbook[sheet_name]
          for row in excel_sheet.iter_rows(min_row=1, max_col=excel_sheet.max_column, max_row=excel_sheet.max_row):
            for cell in row:
              font = cell.font
              if font.name not in font_names_list: 
                font_names_list.append(font.name)
  except Exception as e:
    print(f"Error reading {excel_file}: {str(e)}")
  return font_names_list

#TODO
def get_chart_data(excel_files):
  # chart_data_list = []
  #   # Go through each file in the given list of excel files
  # for file in excel_files:
  #   try:
  #     # If the file has no filename, something went wrong
  #     if file.filename == "":
  #       print(f"Could not retrieve filename from {file}")
  #     else:
  #       # Otherwise save the file, open the workbook, and get the formula from every cell which contains a formula
  #       if file:
  #         file_chart_list = []
  #         assignment_files_folder = "scan_assignment_uploads"
  #         assignment_file_path = os.path.join(assignment_files_folder, file.filename)
  #         excel_workbook = load_workbook(assignment_file_path)
  #         for sheet in excel_workbook:
  #           for chart in sheet._charts:
  #   except Exception as e:
  #     print(f"Error reading {file}: {str(e)}")
  return chart_data_list

def get_formula_data(excel_file):
  file_formula_list = []
  try:
    # If the file has no filename, something went wrong
    if excel_file.filename == "":
      print(f"Could not retrieve filename from {excel_file}")
    else:
      # Otherwise save the file, open the workbook, and get the formula from every cell which contains a formula
      if excel_file:
        assignment_files_folder = "scan_assignment_uploads"
        assignment_file_path = os.path.join(assignment_files_folder, excel_file.filename)
        excel_workbook = load_workbook(assignment_file_path)
        for sheet_name in excel_workbook.sheetnames:
          excel_sheet = excel_workbook[sheet_name]
          for row in excel_sheet.iter_rows(min_row=1, max_col=excel_sheet.max_column, max_row=excel_sheet.max_row):
            for cell in row:
              if cell.data_type == "f":
                file_formula_list.append(cell.value)
  except Exception as e:
    print(f"Error reading {file_formula_list}: {str(e)}")
  return file_formula_list
