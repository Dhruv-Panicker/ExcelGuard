from .fingerprint import check_fingerprint
from .column_width import check_column_width
from .author_data import check_author_data
from .shape_data import check_shape_data
from .font_data import check_font_data
from .link_data import check_link_data
from .formula_data import check_formula_data

# algorithm/plagiarism_checker.py
#Function that will get all data from the beign_scan function 
def get_file_data(author_data, column_data, font_data, formula_data, chart_data):
    file_data = {
        'author_data': author_data,
        'column_data': column_data,
        'font_data': font_data,
        'formula_data': formula_data,
        'chart_data': chart_data
    }
    return file_data

def get_template_file_data(author_data, column_data, font_data, formula_data, chart_data):
    template_file_data = {
        'author_data': author_data,
        'column_data': column_data,
        'font_data': font_data,
        'formula_data': formula_data,
        'chart_data': chart_data
    }
    return template_file_data


#THIS IS A PLACEHOLDER FUNCTION THAT WILL JUST CALL AND AGGREGATE ALL THE CHECKS 
def perform_checks(file_data, template_file_data):
    # Calculate scores from each individual check
    fingerprint_score = check_fingerprint(file_data)
    column_width_files = check_column_width(file_data['column_data'], template_file_data['column_data'])
    author_data_score = check_author_data(file_data)
    shape_data_score = check_shape_data(file_data)
    font_data_score = check_font_data(file_data)
    link_data_score = check_link_data(file_data)
    formula_data_score = check_formula_data(file_data)

    # Aggregate the scores.
    total_score = (fingerprint_score + column_width_files + author_data_score +
                   shape_data_score + font_data_score + link_data_score +
                   formula_data_score) / 7  # Example averaging 

    # Return the total score
    return total_score


