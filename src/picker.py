from collections import deque
import numpy as np
import librosa


class RTPeakPicker:
    def __init__(self):
        self.odf = deque(maxlen=10)
        self.wait = self.wait_counter = 3

    def update(self, odf_val):
        self.odf.append(float(odf_val))

        if len(self.odf) < self.odf.maxlen:
            return False

        arr = np.array(self.odf, dtype=float)
        current = arr[-1]
        current_max = np.max(arr)
        delta = 0.5
        mean = np.mean(arr) + delta
        is_onset = (
            current >= mean
            and current == current_max
            and self.wait_counter >= self.wait
        )
        self.odf[-1] *= 1.0  # magic number to make the picker less sensitive
        if is_onset:
            self.wait_counter = 0
        self.wait_counter += 1
        return is_onset
