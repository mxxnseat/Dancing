import sys
import time
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import QTimer, Qt
from multiprocessing import Value


class Animator:
    def __init__(self, value: Value):
        self.value = value
        self.app = QApplication(sys.argv)
        self.frames_to_play = 0

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.resize(300, 300)

        self.movie = QMovie("./assets/drum-cat.gif")
        self.movie.setCacheMode(QMovie.CacheMode.CacheAll)
        self.label.setMovie(self.movie)
        self.movie.frameChanged.connect(self.on_frame)

        self.label.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.process_queue)
        self.timer.start(0)

    def on_frame(self, frame: int):
        if self.frames_to_play <= 0:
            return
        self.frames_to_play -= 1

        if self.frames_to_play == 0:
            self.movie.stop()

    def play(self):
        self.frames_to_play = 16
        self.movie.stop()
        self.movie.start()

    def process_queue(self):
        if self.value.value:
            self.play()
            self.value.value = False

    def start(self):
        self.app.exec()
