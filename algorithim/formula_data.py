import re
import math
from collections import defaultdict


def determine_threshold(formula, num_files):
    """
        Function to determine plagiarism threshold for a formula

        Args:
            formula: string
            num_files: int

        Returns:
            threshold integer - number of matches to be deemed suspicious
    """
    base_threshold = math.ceil(int(num_files * 0.05))
    threshold = math.ceil(base_threshold + (len(formula) - 40) * 0.0025)
    return threshold


def find_matching_token_lists(dict1, dict2, flagged_formulas):
    """
        Function to find matching token lists in two separate dictionaries

        Args:
            dict1: dictionary of tokens
            dict2: dictionary of tokens

        Returns:
            matching_lists: list of matches (formula position in respective file)
    """
    matching_lists = []

    # Iterate through each key-value pair in the first dictionary
    for key1, token_list1 in dict1.items():

        # Iterate through each key-value pair in the second dictionary
        for key2, token_list2 in dict2.items():

            # Check if the token lists match
            if token_list1 == token_list2:
                matching_lists.append((key1, key2))
                formula = "".join(token_list1)

                if formula in flagged_formulas:
                    flagged_formulas[formula] += 1
                else:
                    flagged_formulas[formula] = 1

    return matching_lists


def tokenize_strings(dictionary):
    """
        Function to tokenize dictionary of strings

        Args:
            dictionary: dictionary of strings (formulas)

        Returns:
            tokenized_dict: dictionary containing lists of tokenized strings
    """
    tokenized_dict = defaultdict(list)

    for key in dictionary:
        tokens = tokenize_formula(dictionary[key])
        tokenized_dict[key] = tokens

    return tokenized_dict


def tokenize_formula(formula_data):
    """
        Function to tokenize strings

        Args:
            formula_data: formula

        Returns:
            tokens: formula as a list of tokens
    """
    tokens = {}
    tokens = re.findall(r'([A-Z]+|[0-9]+(?:\.[0-9]+)?|\(|\)|,|[-+*/^=]|[A-Z]+[0-9]+)', formula_data)
    return tokens


def check_formula_data(formula_data, db, ExcelFile):
    """
        Function to compare excel file formulas in a scan

    """

    suspicious_formulas = {}
    tokenized_formulas = {}
    tokenized_comp_formulas = {}

    # Get the number of files
    number_of_files = len(formula_data)

    # Loop through each file
    for file_id, formulas in formula_data.items():

        # Get the file's name
        file_name = ExcelFile.query.get(file_id).file_name

        # Flagged messages list for each file
        flagged_messages = []

        # Tokenize each formula associated with each file
        tokenized_formulas = tokenize_strings(formulas)

        # Keep track of unique formulas flagged
        flagged_formulas = {}

        # Compare with each other file in the associated scan
        for file_id_comp, formulas_comp in formula_data.items():

            # Get the compared file's name
            file_comp_name = ExcelFile.query.get(file_id_comp).file_name

            # Compare with each other file (not itself)
            if file_id != file_id_comp:

                # Tokenize comparison file's formulas
                tokenized_comp_formulas = tokenize_strings(formulas_comp)

                # Check for matches between the two files, fill flagged_files with matched formulas
                matching_tokens = find_matching_token_lists(tokenized_formulas, tokenized_comp_formulas, flagged_formulas)

                # If matches exists
                if matching_tokens:

                    # For each match create a flagged message
                    for match in matching_tokens:

                        # Tokenize the formula
                        token_match = tokenize_formula(formulas[match[0]])

                        # Turn the tokenized list into a string
                        match_string = "".join(token_match)

                        # See how many matches the formula has within the other excel files
                        match_count = flagged_formulas[match_string]

                        # Determine the threshold for the formula
                        threshold = determine_threshold(match_string, number_of_files)

                        # If the number of matches is less than or equal to the threshold - deem suspicious
                        if match_count <= threshold:

                            message = f"File {file_name} and {file_comp_name} share similar formula structures in cells {match[0]}, {match[1]} with formulas: ({formulas[match[0]]}), ({formulas_comp[match[1]]})."

                            # Add to flagged messages
                            flagged_messages.append(message)

        # Get the number of flags
        num_of_flags = len(flagged_messages)

        # Fill suspicious formulas
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








