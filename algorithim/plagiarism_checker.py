from .fingerprint_data import check_fingerprint_data
from .column_data import check_column_data
from .author_data import check_author_data
from .shape_data import check_shape_data
from .font_data import check_font_data
from .link_data import check_link_data
from .formula_data import check_formula_data

#THIS IS A PLACEHOLDER FUNCTION THAT WILL JUST CALL AND AGGREGATE ALL THE CHECKS 
def perform_checks(file_data):
  # Calculate scores from each individual check
  fingerprint_score = check_fingerprint_data(file_data)
  column_width_score = check_column_data(file_data)
  author_data_score = check_author_data(file_data)
  shape_data_score = check_shape_data(file_data)
  font_data_score = check_font_data(file_data)
  link_data_score = check_link_data(file_data)
  formula_data_score = check_formula_data(file_data)

  # Aggregate the scores.
  total_score = (fingerprint_score + column_width_score + author_data_score +
                  shape_data_score + font_data_score + link_data_score +
                  formula_data_score) / 7  # Example averaging 

  # Return the total score
  return total_score


