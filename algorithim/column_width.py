def check_coloumn_data(file_column_data, template_column_data):
    #Set where all the suspicious files will be added 
    suspicious_files = set()

    #Convert the template file coloumn data into a set for lookup 
    template_column_data = set(template_column_data)

    # Store a dictionary mapping the column width set to the filenames that have it
    column_set_to_files = {}

    for filename, columns in file_column_data.items(): 
        if set(columns) == template_column_data: 
            continue
        # hashable version of a set that can be used as a key in a dictionary.
        column_width_key = frozenset(columns)  

        if column_width_key not in column_set_to_files: 
            column_set_to_files[column_width_key] = {filename}
        else: 
            #If the theres already a file with this coloumn width then mark it as suspicious
            column_set_to_files[column_width_key].add(filename)
            suspicious_files.update(column_set_to_files[column_width_key])
    
    return list(suspicious_files)
