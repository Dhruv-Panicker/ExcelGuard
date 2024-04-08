import sys
import os
# Add the project root directory to the sys.path list
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from algorithim.plagiarism_checker import perform_checks
from unittest.mock import patch
from main import db, ExcelFile

mock_fingerprint_scores = {
    "file1.xlsx": [("fingerprint", "fingerprint match", 3)],
    "file2.xlsx": [("fingerprint", "fingerprint match", 3)]
}
print(mock_fingerprint_scores)

mock_column_width_scores = {
    "file1.xlsx": [('column_width', [10, 20, 30], 2)]
}

mock_author_scores = {
    "file2.xlsx": [('author_data', 'same_creator:userA', 3)]
}

mock_font_scores = {
    "file3.xlsx": [('font_data', 'Agency FB', 1)]
}

mock_formula_scores = {

}

# Expected final ranking based on mock data and weights
expected_ranking = {
    "file2.xlsx": {"reasons": ["fingerprint match", "same_creator:userA"], "score": 15},
    "file1.xlsx": {"reasons": ["fingerprint match", [10, 20, 30]], "score": 13},
    "file3.xlsx": {"reasons": ["Agency FB"], "score": 1}
}



def test_perform_checks_ranking():
    # Combining all scores
    all_scores = {}
    for scores_dict in [mock_fingerprint_scores, mock_column_width_scores, mock_author_scores, mock_font_scores, mock_formula_scores]:
        for key, value in scores_dict.items():
            if key in all_scores:
                all_scores[key].extend(value)
            else:
                all_scores[key] = value
    print(all_scores)

    final_scores = {}
    # Weights of each component
    weights = {
        "fingerprint": 3,
        "column_width": 2,
        "author_data": 2,
        "shape_data": 2,
        "font_data": 1,
        "link_data": 3,
        "formula_data": 2
    }

    # Aggregating scores from all components
    for file, components in all_scores.items():
        if file not in final_scores:
            final_scores[file] = {"reasons": [], "score": 0}
        for detail in components:
            component_type, reason, score = detail  
            final_scores[file]["reasons"].append(reason)
            final_scores[file]["score"] += score * weights[component_type]

    # Rank files based on the total score
    ranked_files = sorted(final_scores.items(), key=lambda x: x[1]['score'], reverse=True)
    ranked_files_dict = {file: details for file, details in ranked_files}

    assert ranked_files_dict == expected_ranking, f"The ranking does not match the expected output. Got {ranked_files_dict}"

   

