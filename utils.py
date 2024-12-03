from typing import Optional

CHUNK = 512
SAMPLE_RATE = 44100

NOTES = {
    "F,": 174.61,
    "^F,": 185.00, "G,": 196.00, "^G,": 207.65, "A,": 220.00, "^A,": 233.08, "B,": 246.94,
    "C": 261.63, "^C": 277.18, "D": 293.66, "^D": 311.13, "E": 329.63, "F": 349.23,
    "^F": 369.99, "G": 392.00, "^G": 415.30, "A": 440.00, "^A": 466.16, "B": 493.88,
    "c": 523.25, "^c": 554.37, "d": 587.33, "^d": 622.25, "e": 659.25, "f": 698.46,
    "^f": 739.99, "g": 783.99, "^g": 830.61, "a": 880.00, "^a": 932.33, "b": 987.77,
    "c'": 1046.50
}

def find_nearest_note(frequency: float) -> Optional[str]:
    if frequency is None or frequency <= 0:
        return None
    
    min_diff = float("inf")
    nearest_note = None
    
    for note, note_freq in NOTES.items():
        diff = abs(frequency - note_freq)
        if diff < min_diff:
            min_diff = diff
            nearest_note = note
    
    return nearest_note