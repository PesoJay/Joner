# Algorithm based on
# A. de Cheveigné and H. Kawahara. "YIN, a fundamental frequency estimator for speech and music"
# The Journal of the Acoustical Society of America 111.4 (2002)

import numpy as np
from typing import Optional

#Calculate the difference function for all offset values
def difference_function(data: np.ndarray, offset_max: int) -> np.ndarray:
    result = np.zeros(offset_max)
    for offset in range(1, offset_max):
        for j in range(len(data) - offset_max):
            difference = data[j] - data[j + offset]
            result[offset] += difference * difference
    return result

# Calculate the cmdf for all offset values
def cumulative_mean_normalized_difference_function(df: np.ndarray) -> np.ndarray:
    cmdf = np.ones(len(df), float)
    running_sum = 0.0
    
    for offset in range(1, len(df)):
        running_sum += df[offset]
        if running_sum != 0:
            cmdf[offset] = df[offset] * offset / running_sum      
    
    return cmdf

# Find first offset where offset < threshold, then find local minimum
def absolute_threshold(cmdf: np.ndarray, threshold: float = 0.1) -> Optional[int]:
    for offset in range(1, len(cmdf)):
        if cmdf[offset] < threshold:
            while offset + 1 < len(cmdf) and cmdf[offset + 1] < cmdf[offset]:
                offset += 1
            return offset
    return None

def get_pitch_yin(data: np.ndarray, sample_rate: int, threshold: float = 0.1) -> Optional[float]:   
    data = data - np.mean(data)
    offset_max = len(data) // 2
    
    df = difference_function(data, offset_max)
    cmdf = cumulative_mean_normalized_difference_function(df)
    offset = absolute_threshold(cmdf, threshold)

    # Parabolic Interpolation for higher accuracy
    if offset is not None:
        if offset > 0 and offset < len(cmdf) - 1:
            alpha = cmdf[offset - 1]
            beta = cmdf[offset]
            gamma = cmdf[offset + 1]
            peak = offset + (gamma - alpha) / (2 * (2 * beta - gamma - alpha))
            return sample_rate / peak
    
    return None