def check_author_data(author_data, template_author_data):
    suspicious_files  = []

    template_create_date = template_author_data.get("created", None)

    for filename, authordata in author_data.items(): 
        
        file_created_date = authordata.get("created", None)
        file_last_modified = authordata.get("lastModifiedBy", None)
        file_creator = authordata.get("creator", None)

        #Check if the student file was even made before creation og the template file 
        if file_created_date < template_create_date: 
            suspicious_files.add(filename, f"Created before the template file date {template_create_date}")
            
        
        #Loop through comparison of the other files 
        for comparison_file, comparison_data in author_data.items():
                if filename != comparison_file: 
                    comparison_creator = comparison_data.get("creator")
                    comparison_last_modified = comparison_data.get("lastModifiedBy")
                    comparison_created_date = comparison_data.get("created")

                    #Check if files have the same creator 
                    if file_creator == comparison_creator and file_creator != None: 
                         suspicious_files.append((filename, f"same_creator:{file_creator}"))
                    #Check if files have the same last modified 
                    if file_last_modified == comparison_last_modified and file_last_modified != None: 
                        suspicious_files.append((filename, f"same_last_modified_by:{file_last_modified}"))
                    #Check if two files were created at the exact same time
                    if file_created_date == comparison_created_date != None: 
                        suspicious_files.append((filename, f"same_creation_date:{file_created_date}"))
                        

    return suspicious_files