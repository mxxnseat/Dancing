from socket import if_nameindex
import numpy as np


class Beep:
    def __init__(self, sr, output_size, is_on=False):
        self.is_on = is_on
        self.sine_pos = 0
        self.play_sine = False

        self.SINE_FREQ = 1000
        self.SINE_LEN = int(0.05 * sr)  # 100ms beep
        self.t = np.arange(self.SINE_LEN) / sr
        self.SINE = 0.6 * np.sin(2 * np.pi * self.SINE_FREQ * self.t).astype(np.float32)
        self.last_out = np.zeros(output_size, dtype=np.float32)
        self.beep_active = False
        self.beep_pos = 0

    def activate(self):
        self.beep_active = True

    def play(self, outdata, frames):
        outdata.fill(0.0)
        if not self.beep_active or not self.is_on:
            return

        remaining = self.SINE_LEN - self.beep_pos
        n = min(frames, remaining)

        # Add beep
        outdata[:n, 0] += self.SINE[self.beep_pos : self.beep_pos + n]
        self.beep_pos += n

        if self.beep_pos >= self.SINE_LEN:
            self.beep_active = False
            self.beep_pos = 0
