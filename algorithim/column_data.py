def check_column_width(file_column_data, template_column_data):
    suspicious_files = set()
    
    # Convert the template_column_data into a set 
    template_column_set = set(template_column_data)

    # Store a dictionary mapping the column width set to filenames 
    column_set_to_files = {}

    for filename, columns in file_column_data.items():
        # Skip files that match the template widths
        if set(columns) == template_column_set:
            continue
        # immutable and hashable version of a set that can be used as a key in a dictionary.    
        column_width_key = frozenset(columns)  

        if column_width_key not in column_set_to_files:
            column_set_to_files[column_width_key] = {filename}
        else:
            # If there's already a file with this column width set, it's suspicious
            column_set_to_files[column_width_key].add(filename)
            suspicious_files.update(column_set_to_files[column_width_key])

    return list(suspicious_files)
