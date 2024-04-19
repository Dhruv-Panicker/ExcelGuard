from itertools import combinations

def check_author_data(author_data, db, ExcelFile, template_author_data):
  suspicious_files = {}

  template_create_date = None
  if template_author_data is not None:
    template_create_date = template_author_data.get("created")
    template_create_date_str = template_create_date.strftime('%m/%d/%Y') if template_create_date else None

  for file1, file2 in combinations(author_data.items(), 2):
    flagged_messages = {}
    file_id1, author_data1 = file1
    file_id2, author_data2 = file2
    file1_name = author_data1["file_name"]
    file2_name = author_data2["file_name"]

    if template_create_date is not None: 
      if author_data1["created"] < template_create_date:
        flagged_messages.setdefault(file_id1, []).append((f"Created before the template file date: {template_create_date_str}", 1))

    if author_data1["creator"] == author_data2["creator"] and author_data1["creator"] != "Microsoft Office User":
      flagged_messages.setdefault(file_id1, []).append((f"Same creator: {author_data1['creator']} as {file2_name}", 3))
      flagged_messages.setdefault(file_id2, []).append((f"Same creator: {author_data2['creator']} as {file1_name}", 3))

    if author_data1["lastModifiedBy"] == author_data2["lastModifiedBy"] and author_data1["lastModifiedBy"] != "Microsoft Office User":
      flagged_messages.setdefault(file_id1, []).append((f"Same last modified by: {author_data1['lastModifiedBy']} as {file2_name}", 2))
      flagged_messages.setdefault(file_id2, []).append((f"Same last modified by: {author_data2['lastModifiedBy']} as {file1_name}", 2))

    if author_data1["created"] == author_data2["created"]:
      auth1_str = author_data1["created"].strftime('%m/%d/%Y')
      auth2_str = author_data2["created"].strftime('%m/%d/%Y')
      flagged_messages.setdefault(file_id1, []).append((f"Same creation date: {auth1_str} as {file2_name}", 2))
      flagged_messages.setdefault(file_id2, []).append((f"Same creation date: {auth2_str} as {file1_name}", 2))
      
    for file_id, reasons_list in flagged_messages.items():
      reasons = [reason for reason, _ in reasons_list]
      if file_id in suspicious_files:
        existing_reasons = suspicious_files[file_id][1]
        reasons = reasons + existing_reasons
      max_score = max(score for _, score in reasons_list)
      suspicious_files[file_id] = ("author_data", reasons, max_score)

    try:
      excel_file1 = db.session.query(ExcelFile).filter_by(id=file_id1).first()
      excel_file2 = db.session.query(ExcelFile).filter_by(id=file_id2).first()
      if excel_file1 and file_id1 in suspicious_files:
        excel_file1.author_data_results = suspicious_files[file_id1]
        db.session.commit()
      if excel_file2 and file_id2 in suspicious_files:
        excel_file2.author_data_results = suspicious_files[file_id2]
        db.session.commit()
    except Exception as e:
      db.session.rollback()
      print("Error updating excel file author data results attribute:", e)

  return suspicious_files
