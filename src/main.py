import sounddevice as sd
import threading
import numpy as np
from animator import Animator
from multiprocessing import Process, Queue, Value
from beep import Beep
from rhytm import Rhytm

BLOCK_SIZE = 2048
HOP_SIZE = 512
device_index = 0
dev = sd.query_devices(device_index)
sr = int(dev["default_samplerate"])


def audio_process(shared_value, rhytm, beep):
    stop = threading.Event()

    def audio_callback(indata, outdata, frames, time_info, status):
        mono = indata[:, 0]
        for hit in rhytm.detectDrum(mono):
            if hit:
                beep.activate()
                shared_value.value = True
        beep.play(outdata, frames)

    with sd.Stream(
        device=(0, 2),
        channels=(1, 1),
        samplerate=sr,
        callback=audio_callback,
        blocksize=BLOCK_SIZE,
    ):
        print("Playing forever... Ctrl+C to stop")
        stop.wait()


if __name__ == "__main__":
    beep = Beep(sr, BLOCK_SIZE, True)
    shared_value = Value("b", False)

    animator = Animator(shared_value)
    rhytm = Rhytm(sr, n_fft=BLOCK_SIZE, hop=HOP_SIZE)

    poll_queue_process = Process(target=audio_process, args=(shared_value, rhytm, beep))
    poll_queue_process.start()
    animator.start()
