def check_author_data(author_data, template_author_data):
    suspicious_files  = set()

    template_create_date = template_author_data.get("created", None)

    for filename, authordata in author_data.items(): 
        
        file_created_date = authordata.get("created", None)
        file_last_modified = authordata.get("lastModifiedBy", None)
        file_creator = author_data.get("creator", None)

        #Check if the student file was even made before creation og the template file 
        if file_created_date < template_create_date: 
            suspicious_files.add(filename)
            continue
        
        #Loop through comparison of the other files 
        for comparison_file, comparison_author_data in author_data.items(): 
            #Check if files have the same creator 
            if file_creator == comparison_author_data.get("creator"): 
                suspicious_files.add(filename)
                suspicious_files.add(comparison_file)
            #Check if files have the same last modified 
            if file_last_modified == comparison_author_data.get("lastModifiedBy"): 
                suspicious_files.add(filename)
                suspicious_files.add(comparison_file)
            #Check if two files were created at the exact same time
            if file_created_date == comparison_author_data.get("created"): 
                suspicious_files.add(filename)
                suspicious_files.add(comparison_file)

    return list(suspicious_files)