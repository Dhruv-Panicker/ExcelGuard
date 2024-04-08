import hashlib 

# Using a hash function to generate fingerprint 
def generate_fingerprint(author_data, formula_data): 
  data_string = f"{author_data}{formula_data}"

  fingerprint = hashlib.sha256(data_string.encode()).hexdigest()

  return fingerprint


def check_fingerprint_data(fingerprint_data, db, ExcelFile):
  suspicious_files = {}
  fingerprint_to_file = {}

  # Iterarate through all the files  
  for file_id, data in fingerprint_data.items():
    # Generate the fingerprint for each file 
    fingerprint = generate_fingerprint(data['author_data'], data['formula_data'])
    #If fingerprint is found already in the dictionary then flag that file 
    if fingerprint in fingerprint_to_file: 
      # Flag the current file and the file to which it was matched with into the set 
      matched_file = fingerprint_to_file[fingerprint]
      
      if file_id not in fingerprint_to_file: 
        suspicious_files[file_id] = ("fingerprint", f"matched_fingerprint_with:{matched_file}", 3)

      if matched_file not in suspicious_files: 
        suspicious_files[matched_file] = ("fingerprint", f"matched_fingerprint_with:{file_id}", 3)
        
    else: 
      # Otherwise add that unique fingerprint and associated file_id to the dictionary 
      fingerprint_to_file[fingerprint] = file_id
  return suspicious_files