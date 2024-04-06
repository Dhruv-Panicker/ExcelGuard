from itertools import combinations
from datetime import datetime

def check_author_data(author_data, template_author_data):
  suspicious_files = {}

  template_create_date = template_author_data.get("created")
  template_create_date_str = template_create_date.strftime('%m/%d/%Y') if template_create_date else None

  for file1, file2 in combinations(author_data.items(), 2):
    filename1, author_data1 = file1
    filename2, author_data2 = file2

    if author_data1["created"] < template_create_date:
      suspicious_files.setdefault(filename1, []).append(f"Created before the template file date {template_create_date_str}")

    if author_data1["creator"] == author_data2["creator"]:
      suspicious_files.setdefault(filename1, []).append(f"same_creator:{author_data1['creator']}")
      suspicious_files.setdefault(filename2, []).append(f"same_creator:{author_data2['creator']}")

    if author_data1["lastModifiedBy"] == author_data2["lastModifiedBy"]:
      suspicious_files.setdefault(filename1, []).append(f"same_last_modified_by:{author_data1['lastModifiedBy']}")
      suspicious_files.setdefault(filename2, []).append(f"same_last_modified_by:{author_data2['lastModifiedBy']}")

    if author_data1["created"] == author_data2["created"]:
      suspicious_files.setdefault(filename1, []).append(f"same_creation_date:{author_data1['created']}")
      suspicious_files.setdefault(filename2, []).append(f"same_creation_date:{author_data2['created']}")

  return suspicious_files
