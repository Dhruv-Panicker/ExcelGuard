def check_column_width(file_column_data, db, ExcelFile, template_column_data):
    suspicious_details = []
    template_column_set = set(template_column_data)

    # Iterate through each pair of files
    for filename1, columns1 in file_column_data.items():
        for filename2, columns2 in file_column_data.items():
            if filename1 == filename2:
                continue  # Skip comparing the file with itself

            # Find common columns between the two files that are not in the template
            common_unique_columns = set(columns1).intersection(columns2) - template_column_set

            if common_unique_columns:
                # If there are common columns not in the template, flag both files
                suspicious_details.append((filename1, tuple(common_unique_columns)))
                suspicious_details.append((filename2, tuple(common_unique_columns)))

    # Remove duplicates while preserving order
    seen = set()
    suspicious_files = {}
    for filename, column_set in suspicious_details:
        if (filename, column_set) not in seen:
            # Convert tuple back to list for output
            if len(column_set) >= 3: 
                suspicious_files[filename] = (list(column_set), 3)
            else: 
                suspicious_files[filename] = (list(column_set), 1)
            seen.add((filename, column_set))

    return suspicious_files
