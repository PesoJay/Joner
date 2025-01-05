import numpy as np
from scipy.fftpack import fft
from typing import List, Optional, Tuple
from utils import NOTES, CHORD_PATTERNS, find_nearest_note

def get_note_frequencies(data: np.ndarray, sample_rate: int, num_peaks: int = 6) -> List[float]:
    window = np.hanning(len(data))
    data = data * window
    
    fft_data = fft(data)
    frequencies = np.fft.fftfreq(len(data), 1/sample_rate)
    
    positive_frequencies = []
    for frequency in frequencies:
        if frequency >= 0:
            positive_frequencies.append(frequency)

    frequencies = positive_frequencies

    magnitudes = []
    for i, frequency in enumerate(frequencies):
        magnitudes.append(abs(fft_data[i]))

    magnitudes = magnitudes / np.max(magnitudes)
    
    peak_indices = []
    threshold = 0.1
    
    for i in range(1, len(magnitudes) - 1):
        if (magnitudes[i] > threshold and 
            magnitudes[i] > magnitudes[i-1] and 
            magnitudes[i] > magnitudes[i+1]):
            peak_indices.append(i)
    
    if not peak_indices:
        return []
    
    peak_indices.sort(key=lambda x: magnitudes[x], reverse=True)
    peak_indices = peak_indices[:num_peaks]
    
    frequencies = []
    # Parabolic Interpolation for higher accuracy
    for peak_index in peak_indices:
        if peak_index > 0 and peak_index < len(magnitudes) - 1:
            alpha = magnitudes[peak_index - 1]
            beta = magnitudes[peak_index]
            gamma = magnitudes[peak_index + 1]
            
            p = (gamma - alpha) / (2 * (2 * beta - gamma - alpha))
            exact_frequency = (peak_index + p) * sample_rate / len(data)
            
            if 80 <= exact_frequency <= 2300:
                frequencies.append(exact_frequency)
    
    return frequencies

def find_notes_in_chord(frequencies: List[float]) -> List[str]:
    notes = []
    for frequency in frequencies:
        nearest_note = find_nearest_note(frequency)
        
        if nearest_note and nearest_note not in notes:
            notes.append(nearest_note)
    
    return notes

def identify_chord(notes: List[str]) -> Optional[Tuple[str, str]]:
    if len(notes) < 3:
        return None
        
    root_note = min(notes, key=lambda x: NOTES[x])
    root_frequency = NOTES[root_note]
    
    # Calculate the number of semitone steps from root note to other notes
    intervals = []
    for note in notes:
        frequency = NOTES[note]
        semitones = round(12 * np.log2(frequency / root_frequency))
        intervals.append(semitones % 12)
        
    for chord_name, pattern in CHORD_PATTERNS.items():
        chord_found = True
        for i in pattern:
            if i not in intervals:
                chord_found = False
                break

        if chord_found:
            return root_note, chord_name
    
    return None