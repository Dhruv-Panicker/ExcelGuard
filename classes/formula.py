import re


class Formula:
  def __init__(self, formula_string):
    # Store formula as a string
    self.formula = formula_string

    # Store formula as tokens
    self.tokenized = re.findall(r'([A-Z]+|[0-9]+(?:\.[0-9]+)?|\(|\)|,|[-+*/^]|[A-Z]+[0-9]+)', formula_string)

  def __str__(self):
    return f"{self.formula}"