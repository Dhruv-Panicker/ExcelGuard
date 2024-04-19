import hashlib 

# Using a hash function to generate fingerprint 
def generate_fingerprint(author_data, formula_data): 
  data_string = f"{author_data}{formula_data}"
  fingerprint = hashlib.sha256(data_string.encode()).hexdigest()

  return fingerprint

def check_fingerprint_data(fingerprint_data, db, ExcelFile):
  suspicious_files = {}
  fingerprint_to_file = {}
  # Iterate through all the files  
  for file_id, data in fingerprint_data.items():
    file_name = data["author_data"]["file_name"]
    # Generate the fingerprint for each file 
    fingerprint = generate_fingerprint(data['author_data'], data['formula_data'])
    # If fingerprint is found already in the dictionary then flag that file 
    if fingerprint in fingerprint_to_file: 
      # Flag the current file and the file to which it was matched with into the set 
      matched_file = fingerprint_to_file[fingerprint]
      matched_file_name = fingerprint_data[matched_file]["author_data"]["file_name"]
      try:
        excel_file = db.session.query(ExcelFile).filter_by(id=file_id).first()
        matched_excel_file = db.session.query(ExcelFile).filter_by(id=matched_file).first()
        
        if file_id not in fingerprint_to_file: 
          suspicious_files[file_id] = ("fingerprint", f"Matched Fingerprint With:{matched_file_name}", 3)
          if excel_file:
            excel_file.fingerprint_results = suspicious_files[file_id]
            db.session.commit()
        if matched_file not in suspicious_files: 
          suspicious_files[matched_file] = ("fingerprint", f"Matched Fingerprint With:{file_name}", 3)
          if matched_excel_file:
            matched_excel_file.fingerprint_results = suspicious_files[matched_file]
            db.session.commit()
      except Exception as e:
        db.session.rollback()
        print("Error updating excel file fingerprint data results attribute:", e)
    else: 
      # Otherwise add that unique fingerprint and associated file_id to the dictionary 
      fingerprint_to_file[fingerprint] = file_id

  return suspicious_files
