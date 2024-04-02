import hashlib 

#Using a hash function to generate fingerprint 
def generate_fingerprint(author_data, formula_data): 
    data_string = f"{author_data}{formula_data}"

    fingerprint = hashlib.sha256(data_string.encode()).hexdigest()

    return fingerprint


def check_fingerprint_data(fingerprint_data):
    suspicious_files = []
    fingerprint_to_file = {}

    #Iterarate through all the files  
    for filename, data in fingerprint_data.items():
        #Generate the fingerprint for each file 
        fingerprint = generate_fingerprint(data['author_data'], data['formula_data'])
        #If fingerprint is found already in the dictionary then flag that file 
        if fingerprint in fingerprint_to_file: 
            #Flag the current file and the file to which it was matched with into the set 
            matched_file = fingerprint_to_file[fingerprint]
            suspicious_files.append((filename, f"matched_fingerprint_with:{matched_file}"))
            suspicious_files.append((matched_file, f"matched_fingerprint_with:{filename}"))
        else: 
            #Otherwise add that unique fingerprint and associated filename to the dictionary 
            fingerprint_to_file[fingerprint] = filename
    return suspicious_files