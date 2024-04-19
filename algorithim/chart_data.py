def check_chart_data(chart_data, db, ExcelFile):
  suspicious_charts = {}
  file_names = [chart['file_name'] for chart_dict in chart_data.values() for chart in chart_dict.values()]

  # Iterate over each chart in each file
  for file_id, charts in chart_data.items():
    flagged_messages = []
    for chart_name, chart_details in charts.items():
      # Get the x and y source filenames for the current chart
      x_source_filename = chart_details.get('x_source_filename')
      y_source_filename = chart_details.get('y_source_filename')
      
      # Check if the x source filename matches any file ID
      if x_source_filename in file_names:
        flagged_messages.append(f"Chart '{chart_name}' has a matching x source filename with file '{x_source_filename}'.")
      
      # Check if the y source filename matches any file ID
      if y_source_filename in file_names:
        flagged_messages.append(f"Chart '{chart_name}' has a matching y source filename with file '{y_source_filename}'.")

    if len(flagged_messages) > 0:
      severity_score = 3
    else:
      severity_score = 0
    suspicious_charts[file_id] = ("chart_data", flagged_messages, severity_score)

    try:
      excel_file = db.session.query(ExcelFile).filter_by(id=file_id).first()
      if excel_file:
        excel_file.chart_data_results = suspicious_charts[file_id]
        db.session.commit()
    except Exception as e:
      db.session.rollback()
      print("Error updating excel file chart data results attribute:", e)

  return suspicious_charts
