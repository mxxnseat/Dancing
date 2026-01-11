import numpy as np
from collections import deque


# 2.3.3 https://mural.maynoothuniversity.ie/id/eprint/4204/1/JT_Real-Time_Detection.pdf
class ComplexDomainODF:
    def __init__(self, sr: int, n_fft: int, hop: int, fmin=20.0, fmax=200.0):
        self.sr = sr
        self.n_fft = n_fft
        self.hop = hop

        self.window = np.hanning(n_fft).astype(np.float32)

        freqs = np.fft.rfftfreq(n_fft, d=1.0 / sr)
        self.mask = (freqs >= fmin) & (freqs <= fmax)

        self.prev_phases = deque(maxlen=2)
        self.prev_magnitude = None

    def wrap_phase(self, phase: float) -> float:
        return (phase + np.pi) % (2 * np.pi) - np.pi

    def process_frame(self, frame: np.ndarray) -> float:
        windowed_frame = frame.astype(np.float32) * self.window
        X = np.fft.rfft(windowed_frame).astype(np.complex64)
        mag = np.abs(X)
        phi = np.angle(X)

        if self.prev_magnitude is None:
            self.prev_magnitude = mag
            self.prev_phases.append(phi)
            return 0.0

        if len(self.prev_phases) < 2:
            self.prev_phases.append(phi)
            self.prev_magnitude = mag
            return 0.0

        phi_hat = (2 * self.prev_phases[-1]) - self.prev_phases[-2]
        dmag = np.maximum(0.0, mag - self.prev_magnitude)

        cos_term = np.cos(self.wrap_phase(phi - self.wrap_phase(phi_hat)))

        power = mag**2
        prev_power = self.prev_magnitude**2
        gamma = np.sqrt(power + prev_power - (2 * mag * self.prev_magnitude * cos_term))
        odf = np.sum(dmag * gamma)
        self.prev_magnitude = mag
        self.prev_phases.append(phi)
        return odf
