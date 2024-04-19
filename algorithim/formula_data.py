import re
from collections import defaultdict


def find_matching_token_lists(dict1, dict2):
    matching_lists = []

    # Iterate through each key-value pair in the first dictionary
    for key1, token_list1 in dict1.items():
        # Iterate through each key-value pair in the second dictionary
        for key2, token_list2 in dict2.items():
            # Check if the token lists match
            if token_list1 == token_list2:
                matching_lists.append((key1, key2))

    return matching_lists


def tokenize_strings(dictionary):

    tokenized_dict = defaultdict(list)

    for key in dictionary:
        tokens = tokenize_formula(dictionary[key])
        tokenized_dict[key] = tokens

    return tokenized_dict


def tokenize_formula(formula_data):
    tokens = {}
    tokens = re.findall(r'([A-Z]+|[0-9]+(?:\.[0-9]+)?|\(|\)|,|[-+*/^]|[A-Z]+[0-9]+)', formula_data)
    return tokens


def check_formula_data(formula_data, db, ExcelFile):

    suspicious_formulas = {}
    tokenized_formulas = {}
    tokenized_comp_formulas = {}

    for file_id, formulas in formula_data.items():
        file_name = ExcelFile.query.get(file_id).file_name
        # Flagged messages list for each file
        flagged_messages = []

        # Tokenize each formula associated with each file
        tokenized_formulas = tokenize_strings(formulas)

        # Compare with each other file in the associated scan
        for file_id_comp, formulas_comp in formula_data.items():
            file_comp_name = ExcelFile.query.get(file_id_comp).file_name
            # Compare with each other file (not itself)
            if file_id != file_id_comp:

                # Tokenize comparison file's formulas
                tokenized_comp_formulas = tokenize_strings(formulas_comp)

                # Check for matches between the two files
                matching_tokens = find_matching_token_lists(tokenized_formulas, tokenized_comp_formulas)

                # If matches exists
                if matching_tokens:

                    # For each match create a flagged message
                    for match in matching_tokens:
                        flagged_messages.append(f"File {file_name} and {file_comp_name} share similar formula structures in cells {match[0]}, {match[1]} with formulas: ({formulas[match[0]]}), ({formulas_comp[match[1]]}).")

        num_of_flags = len(flagged_messages)
        suspicious_formulas[file_id] = (flagged_messages, num_of_flags)

        try:
            excel_file = db.session.query(ExcelFile).filter_by(id=file_id).first()
            if excel_file:
                excel_file.formula_data_results = suspicious_formulas[file_id]
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Error updating excel file formula data results attribute:", e)

    return suspicious_formulas








