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

def check_font_data(font_data, template_data):
  suspicious_fonts = {}
  template_fonts = set(template_data["font_data"])
  
  for file, fonts in font_data.items():
    similar_fonts = set(font for font in fonts if font not in COMMON_EXCEL_FONTS and font not in template_fonts)
    font_count = len(similar_fonts)
    suspicious_fonts[file] = (similar_fonts, font_count)

  return suspicious_fonts