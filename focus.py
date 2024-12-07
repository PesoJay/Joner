#Copied from Estudio - Martin Karanitsch
constraints = {
    "tonguing": {
        "phrase_allowed_intervals": [0, 1, 2, 3, 4, 7],
        "allowed_note_lengths": [1, 2],
        "figure_allowed_intervals": [-3, -2, -1, 0, 1, 2, 3],
        "allowed_articulation": ["stacc"],
        "attributes": ["equal_note_length", "equal_articulation"]
    },
    "air_column": {
        "phrase_allowed_intervals": [2, 3, 4],
        "allowed_note_lengths": [2],
        "figure_allowed_intervals": [-2, -1, 1, 2],
        "allowed_articulation": ["leg"],
        "attributes": ["long_lines", "equal_articulation", "equal_note_length"]
    },
    "articulation": {
        "phrase_allowed_intervals": [0, 1, 2, 3, 4],
        "allowed_note_lengths": [1, 2, 4],
        "figure_allowed_intervals": [-4, -3, -2, -1, 1, 2, 3, 4],
        "allowed_articulation": ["stacc", "leg"],
        "attributes": ["articulation_change", "min_figure_length_three"]
    },
    "register_change": {
        "phrase_allowed_intervals": [1, 2, 3],
        "allowed_note_lengths": [1, 2],
        "figure_allowed_intervals": [-2, -1, 0, 1, 2],
        "allowed_articulation": ["stacc", "leg"],
        "attributes": ["large_jumps"]
    },
    "technique": {
        "phrase_allowed_intervals": [0, 1, 2, 3],
        "allowed_note_lengths": [1],
        "figure_allowed_intervals": [-3, -2, -1, 1, 2, 3],
        "allowed_articulation": ["leg"],
        "attributes": ["equal_articulation"]
    }
}

def get_constraints(focus: str) -> dict:
    return constraints[focus].copy()