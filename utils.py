from typing import Optional
from etude import Note, Key
from math import floor

YIN_CHUNK = 512
CHORD_CHUNK = 4096
SAMPLE_RATE = 44100

NOTES = {
    "C,,": 65.41, "^C,,": 69.30, "D,,": 73.42, "^D,,": 77.78, "E,,": 82.41, "F,,": 87.31, "^F,,": 92.50, "G,,": 98.00, "^G,,": 103.83, "A,,": 110.00, "^A,,": 116.54, "B,,": 123.47,
    "C,": 130.81, "^C,": 138.59, "D,": 146.83, "^D,": 155.56, "E,": 164.81, "F,": 174.61, "^F,": 185.00, "G,": 196.00, "^G,": 207.65, "A,": 220.00, "^A,": 233.08, "B,": 246.94,
    "C": 261.63, "^C": 277.18, "D": 293.66, "^D": 311.13, "E": 329.63, "F": 349.23, "^F": 369.99, "G": 392.00, "^G": 415.30, "A": 440.00, "^A": 466.16, "B": 493.88,
    "c": 523.25, "^c": 554.37, "d": 587.33, "^d": 622.25, "e": 659.25, "f": 698.46, "^f": 739.99, "g": 783.99, "^g": 830.61, "a": 880.00, "^a": 932.33, "b": 987.77,
    "c'": 1046.50, "^c'": 1108.73, "d'": 1174.66, "^d'": 1244.51, "e'": 1318.51, "f'": 1396.91, "^f'": 1479.98, "g'": 1567.98, "^g'": 1661.22, "a'": 1760.00, "^a'": 1864.66, "b'": 1975.53, "c''": 2093.00, "^c''": 2217.46
}


CHORD_PATTERNS = {
    'major': [0, 4, 7],     
    'minor': [0, 3, 7],     
    'diminished': [0, 3, 6],
    'augmented': [0, 4, 8], 
    'sus4': [0, 5, 7],      
    'sus2': [0, 2, 7],      
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




#Copied from Estudio - Martin Karanitsch

pitch_by_key = { "c": 0, "d": 1, "e": 2, "f": 3, "g": 4, "a": 5, "b": 6 }
pitch_by_val = { 0: "c", 1: "d", 2: "e", 3: "f", 4: "g", 5: "a", 6: "b"}
triads = [
    ["c", "e", "g"], 
    ["d", "f", "a"], 
    ["e", "g", "b"], 
    ["f", "a", "c"], 
    ["g", "b", "d"], 
    ["a", "c", "e"], 
    ["b", "d", "f"]
]
major_functions = {"T": 1, "SP": 2, "DP": 3, "S": 4, "D": 5, "TP": 6}
minor_functions = {"T": 1, "TP": 3, "S": 4, "D": 5, "SP": 6, "DP": 7}
major_degree_modes = {1: "maj", 2: "min", 3: "min", 4: "maj", 5: "maj", 6: "min"}
minor_degree_modes = {1: "min", 3: "maj", 4: "min", 5: "min", 6: "maj", 7: "maj"}
signature = {
        "maj": {
                "C": [], 
                "G": ["F#"], 
                "D": ["F#", "C#"], 
                "A": ["F#", "C#", "D#"], 
                "E": ["F#", "C#", "D#", "A#"],  
                "B": ["F#", "C#", "D#", "A#", "E#"], 
                "F": ["Bb"], 
                "Bb": ["Bb", "Eb"], 
                "Eb": ["Bb", "Eb", "Ab"], 
                "Ab": ["Bb", "Eb", "Ab", "Db"], 
                "Db": ["Bb", "Eb", "Ab", "Db", "Gb"],
        },
        "min": {
                "A": [], 
                "E": ["F#"], 
                "B": ["F#", "C#"], 
                "F#": ["F#", "C#", "D#"],  
                "C#": ["F#", "C#", "D#", "A#"],  
                "G#": ["F#", "C#", "D#", "A#", "E#"],  
                "D": ["Bb"],
                "G": ["Bb", "Eb",],
                "C": ["Bb", "Eb", "Ab"],
                "F": ["Bb", "Eb", "Ab", "Db"],
                "Bb": ["Bb", "Eb", "Ab", "Db", "Gb"],
        }
}


def scale_degree_root(key: Key, degree: int) -> str:
        key_val = pitch_by_key[key.pitch.lower()]
        idx = ( (degree-1) + key_val ) % 7
        pitch = triads[idx][0]
        
        return pitch


def all_pitches_of_degree(degree: int, ambitus: list) -> list:
        pitches = []
        for octave in range(3):
                for note in triads[degree-1]:
                        pitch = pitch_by_key[note] + 7*octave
                        if pitch >= ambitus[0] and pitch < ambitus[1]:
                                pitches.append(pitch)
        return pitches


def relative_pitch(note: Note) -> int:
        return pitch_by_key[note.pitch]


def absolute_pitch(note: Note) -> int:
        return 7 * (note.octave-1) + relative_pitch(note)


def to_relative(pitch_abs: int) -> int:
        return pitch_abs % 7


def note_with_pitch(pitch: int) -> Note:
        pitch_rel = to_relative(pitch)
        octave = floor(pitch/7)+1
        return Note(triads[pitch_rel][0], octave)


def distance(first: Note, second: Note) -> int:
        return absolute_pitch(second) - absolute_pitch(first)


def closest_octave(first: Note, second: Note) -> int:
        first_rel = relative_pitch(first)
        octaves = [note_with_pitch(first_rel), note_with_pitch(first_rel + 7), note_with_pitch(first_rel + 14)]
        min_dist = 99
        min_idx = 0
        for i in range(len(octaves)):
                dist = abs(distance(octaves[i], second))
                if dist < min_dist:
                        min_idx = i
                        min_dist = dist
        return octaves[min_idx]


def function_to_key(function: str, key: Key) -> Key:
        degree = major_functions[function] if key.mode == "maj" else minor_functions[function]
        new_mode = major_degree_modes[degree] if key.mode == "maj" else minor_degree_modes[degree]
        key_signature = signature[key.mode][key.pitch + key.symbol]

        pitch = scale_degree_root(key, degree).upper()
        symbol = ""
        if pitch + "b" in key_signature:
                symbol = "b"
        elif pitch + "#" in key_signature:
                symbol = "#"
        
        new_key: Key = Key(pitch, symbol, new_mode)
        return new_key
