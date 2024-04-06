# A list of 25 commonly used fonts in excel
COMMON_EXCEL_FONTS = {
  "Calibri",
  "Calibri Light",
  "Arial",
  "Times New Roman",
  "Verdana",
  "Tahoma",
  "Cambria",
  "Segoe UI",
  "Helvetica",
  "Garamond",
  "Century Gothic",
  "Comic Sans MS",
  "Courier New",
  "Georgia",
  "Trebuchet MS",
  "Lucida Sans Unicode",
  "Franklin Gothic Medium",
  "Arial Narrow",
  "Impact",
  "Book Antiqua",
  "Consolas",
  "Candara",
  "Arial Black",
  "MS Sans Serif",
  "MS Serif",
  "Palatino Linotype"
}

def check_font_data(font_data, db, template_data, ExcelFile):
  template_fonts = set()
  if template_data:
    template_fonts = set(template_data["font_data"])
  
  for file_id, fonts in font_data.items():
    similar_fonts = set(font for font in fonts if font not in COMMON_EXCEL_FONTS and font not in template_fonts)
    font_count = len(similar_fonts)
    try:
      excel_file = db.session.query(ExcelFile).filter_by(id=file_id).first()
      if excel_file:
        excel_file.font_data_results = (list(similar_fonts), font_count)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      print("Error updating excel file font data results attribute:", e)

  return True