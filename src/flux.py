import numpy as np


class RTSpectralFlux:
    def __init__(self, n_fft=4096):
        self.n_fft = n_fft
        self.prev_mag = None
        self.window = np.hanning(n_fft)
        self.freqs = np.fft.rfftfreq(self.n_fft)
        self.mask = (self.freqs > 20) & (self.freqs < 2000)

    def half_wave_rectify(self, x):
        return (x + np.abs(x)) / 2

    def process_frame(self, frame):
        frame = frame * self.window
        spec = np.fft.rfft(frame)
        delta = 0.3  # experemental value
        mag = np.log1p(delta * np.abs(spec))

        if self.prev_mag is None:
            self.prev_mag = mag
            return 0.0
        flux = self.half_wave_rectify(mag - self.prev_mag).sum()

        self.prev_mag = mag
        return flux
