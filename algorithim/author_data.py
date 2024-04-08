from itertools import combinations
from datetime import datetime

def check_author_data(author_data, db, ExcelFile, template_author_data):
  suspicious_files = {}

  template_create_date = None
  if template_author_data is not None:
    template_create_date = template_author_data.get("created")
    template_create_date_str = template_create_date.strftime('%m/%d/%Y') if template_create_date else None

  for file1, file2 in combinations(author_data.items(), 2):
    file_id1, author_data1 = file1
    file_id2, author_data2 = file2

    if template_create_date is not None: 
      if author_data1["created"] < template_create_date:
        suspicious_files.setdefault(file_id1, []).append((f"Created before the template file date {template_create_date_str}", 1))

    if author_data1["creator"] == author_data2["creator"]:
      suspicious_files.setdefault(file_id1, []).append(("author_data", f"same_creator:{author_data1['creator']}", 3))
      suspicious_files.setdefault(file_id2, []).append(("author_data", f"same_creator:{author_data2['creator']}", 3))

    if author_data1["lastModifiedBy"] == author_data2["lastModifiedBy"]:
      suspicious_files.setdefault(file_id1, []).append(("author_data", f"same_last_modified_by:{author_data1['lastModifiedBy']}", 2))
      suspicious_files.setdefault(file_id2, []).append(("author_data", f"same_last_modified_by:{author_data2['lastModifiedBy']}", 2))

    if author_data1["created"] == author_data2["created"]:
      auth1_str = author_data1["created"].strftime('%m/%d/%Y')
      auth2_str = author_data2["created"].strftime('%m/%d/%Y')
      suspicious_files.setdefault(file_id1, []).append(("author_data", f"same_creation_date:{auth1_str}", 2))
      suspicious_files.setdefault(file_id2, []).append(("author_data", f"same_creation_date:{auth2_str}", 2))
      
  return suspicious_files
