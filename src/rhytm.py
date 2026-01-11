import numpy as np
from flux import RTSpectralFlux
from picker import RTPeakPicker
from odfcd import ComplexDomainODF
import time


class Rhytm:
    def __init__(self, sr=44100, n_fft=4096, hop=512):
        self.sr = sr
        self.n_fft = n_fft
        self.last_hit = 0.0
        self.refactory_sec = 0.07
        self.hop = hop

        self.buf = np.zeros(n_fft)
        self.fluxer = RTSpectralFlux(n_fft)
        self.picker = RTPeakPicker()
        self.odf = ComplexDomainODF(sr, n_fft, hop)

    def detectDrum(self, mono):
        for i in range(0, len(mono) - self.hop + 1, self.hop):
            self.buf[: -self.hop] = self.buf[self.hop :]
            self.buf[-self.hop :] = mono[i : i + self.hop]

            odf = self.fluxer.process_frame(self.buf)
            now = time.time()

            if self.picker.update(odf) and now - self.last_hit > self.refactory_sec:
                self.last_hit = now
                yield True
