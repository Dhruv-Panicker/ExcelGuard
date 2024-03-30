def check_chart_data(chart_data):
  suspicious_charts = {}

  # Get the file names from the chart data dictionary
  file_names = list(chart_data.keys())

  # Iterate over each chart in each file
  for file_name, charts in chart_data.items():
    suspicious_charts[file_name] = []
    for chart_name, chart_details in charts.items():
      # Get the x and y source filenames for the current chart
      x_source_filename = chart_details.get('x_source_filename')
      y_source_filename = chart_details.get('y_source_filename')
      
      # Check if the x source filename matches any file name
      if x_source_filename in file_names:
        x_filename = "x_data_" + x_source_filename
        suspicious_charts[file_name].append(x_filename)  
        print(f"Chart '{chart_name}' in file '{file_name}' has a matching x source filename with file '{x_source_filename}'.")
      
      # Check if the y source filename matches any file name
      if y_source_filename in file_names:
        y_filename = "y_data_" + y_source_filename
        suspicious_charts[file_name].append(y_filename)  
        print(f"Chart '{chart_name}' in file '{file_name}' has a matching y source filename with file '{y_source_filename}'.")

  return suspicious_charts