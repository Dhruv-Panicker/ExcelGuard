import re


class Formula:
  def __init__(self, formula_string):
    # Store formula as a string
    self.formula = formula_string

    # Store formula as tokens
    self.formula_tokens = re.findall(r'[A-Za-z]+|\d+|\S', formula_string)

