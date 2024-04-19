from itertools import combinations

def check_column_width_data(file_column_data, db, ExcelFile, template_column_data):
  suspicious_files = {}
  template_column_set = set(template_column_data)

  # Defining "oddly sized" column widths
  def is_oddly_sized(width):
    return width % 5 != 0

  # Generate combinations of file names
  file_combinations = combinations(file_column_data.keys(), 2)

  for file_id1, file_id2 in file_combinations:
    columns1 = file_column_data[file_id1]["column_widths"]
    columns2 = file_column_data[file_id2]["column_widths"]
    # Filter columns to only include "oddly sized" widths not in the template
    odd_columns1 = set(filter(is_oddly_sized, columns1)) - template_column_set
    odd_columns2 = set(filter(is_oddly_sized, columns2)) - template_column_set

    common_unique_columns = odd_columns1.intersection(odd_columns2)

    if common_unique_columns:
      # If there are common columns not in the template, flag both files
      common_columns_list = list(common_unique_columns)
      for file_id in (file_id1, file_id2):
        if file_id not in suspicious_files:
          suspicious_files[file_id] = ("column_width", [], 0)
          other_file_id = file_id2 if file_id == file_id1 else file_id1
          other_file_name = file_column_data[other_file_id]["file_name"]
          reason = f"Same column widths {common_columns_list} as {other_file_name}"
        # Append the reason and update the score
          suspicious_files[file_id] = list(suspicious_files[file_id])  # convert tuple to list to modify
          suspicious_files[file_id][1].append(reason)
          suspicious_files[file_id][2] = min(len(common_unique_columns), 3)  # cap the score at 3
          suspicious_files[file_id] = tuple(suspicious_files[file_id])  # convert back to tuple
        try:
          excel_file = db.session.query(ExcelFile).filter_by(id=file_id).first()
          if excel_file:
            excel_file.column_data_results = suspicious_files[file_id]
            db.session.commit()
        except Exception as e:
          db.session.rollback()
          print("Error updating excel file column width data results attribute:", e)

  return suspicious_files
