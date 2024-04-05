def check_chart_data(chart_data):
  suspicious_charts = {}

  # Get the file names from the chart data dictionary
  file_names = list(chart_data.keys())

  # Iterate over each chart in each file
  for file_name, charts in chart_data.items():
    flagged_messages = []
    for chart_name, chart_details in charts.items():
      # Get the x and y source filenames for the current chart
      x_source_filename = chart_details.get('x_source_filename')
      y_source_filename = chart_details.get('y_source_filename')
      
      # Check if the x source filename matches any file name
      if x_source_filename in file_names:
        flagged_message = f"Chart '{chart_name}' has a matching x source filename with file '{x_source_filename}'."
        flagged_messages.append(flagged_message) 
      
      # Check if the y source filename matches any file name
      if y_source_filename in file_names:
        flagged_message = f"Chart '{chart_name}' has a matching y source filename with file '{y_source_filename}'."
        flagged_messages.append(flagged_message)  

    count_of_flagged_messages = len(flagged_messages)
    suspicious_charts[file_name] = (flagged_messages, count_of_flagged_messages)

  return suspicious_charts