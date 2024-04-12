from itertools import combinations

def check_column_width_data(file_column_data, db, ExcelFile, template_column_data):
  suspicious_files = {}
  template_column_set = set(template_column_data)

  # Generate combinations of file names
  file_combinations = combinations(file_column_data.keys(), 2)

  for file_id1, file_id2 in file_combinations:
    columns1 = file_column_data[file_id1]
    columns2 = file_column_data[file_id2]

    common_unique_columns = set(columns1).intersection(columns2) - template_column_set

    if common_unique_columns:
      # If there are common columns not in the template, flag both files
      for file_id in (file_id1, file_id2):
        if file_id not in suspicious_files:
          suspicious_files[file_id] = ("column_width", [], 0)
        suspicious_files[file_id][1].extend(common_unique_columns)
        # Convert tuple to list for modification
        suspicious_files[file_id] = list(suspicious_files[file_id])
        suspicious_files[file_id][2] = min(len(common_unique_columns), 3)
        # Convert back to tuple
        suspicious_files[file_id] = tuple(suspicious_files[file_id])
        try:
          excel_file = db.session.query(ExcelFile).filter_by(id=file_id).first()
          if excel_file:
            excel_file.column_data_results = suspicious_files[file_id]
            db.session.commit()
        except Exception as e:
          db.session.rollback()
          print("Error updating excel file column width data results attribute:", e)

  return suspicious_files
