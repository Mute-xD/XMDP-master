import numpy as np
import cv2


class Status:
    def __init__(self):
        self.ctlPower = 0.
        self.ctlAngle = 0.
        self.netPing = 0
        self.stream = None
        self.streamEncoded = None
        self.compressionRate = 0.
        self.running = True
        self.netFPS = 0

    def clear(self):
        pass
