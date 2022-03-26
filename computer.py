import threading
import cv2
import status
import utils
import struct
import numpy as np
import network
import time
import gui
import pygame


NET_STAT_OK = '100'
NET_STAT_CONTINUE = '200'


class DroneMaster:
    def __init__(self):
        self.config = utils.Config('./config.yaml')
        self.status = status.Status()
        self.network = network.NetworkClient(self.config)
        self.ui = gui.GameGUI(self.status)
        self.targetFrame = 1000 // self.config.FRAME
        self.threadNetwork = threading.Thread(target=self.threadNetworkJob)

    def solve(self):
        if self.status.stream is None:
            return
        temp = np.frombuffer(self.status.stream, np.uint8)
        before = len(temp)
        tempDecode = cv2.imdecode(temp, 1)
        after = len(tempDecode)
        self.status.compressionRate = int(before / after)
        tempDecode = cv2.cvtColor(tempDecode, cv2.COLOR_RGB2BGR)
        tempDecode = np.rot90(tempDecode, 1)
        tempDecode = np.flip(tempDecode, 0)
        self.status.streamEncoded = tempDecode

    def exchange(self):
        # ping send
        timeStampSend = int(round(time.time() * 1000))
        self.network.cmdSend(timeStampSend)
        # ping recv
        self.network.cmdRecv()
        # cmd send
        pack = struct.pack('ff', self.status.ctlPower, self.status.ctlAngle)
        self.network.packSend(pack)
        # cmd recv
        ret = self.network.cmdRecv().rstrip()
        if ret != NET_STAT_OK:
            print('ERROR in cmd send')
        # video stream req
        self.network.cmdSend(NET_STAT_CONTINUE)
        # video stream recv size
        ret = int(self.network.cmdRecv())
        self.network.cmdSend(NET_STAT_OK)
        self.status.stream = self.network.dataRecv(ret)
        self.status.netPing = int(round(time.time() * 1000)) - timeStampSend

    def go(self):
        self.ui.initGameWorld()
        self.network.tryConnect()
        self.threadNetwork.start()
        self.threadUIJob()

    def threadUIJob(self):
        while True:
            startTime = pygame.time.get_ticks()
            self.ui.graphRender()
            self.ui.eventProc()
            self.frameRateLimit(startTime)

    def threadNetworkJob(self):
        while True:
            startTime = pygame.time.get_ticks()
            self.exchange()
            self.solve()
            self.frameRateLimit(startTime)
            endTime = pygame.time.get_ticks()
            self.status.netFPS = 1000 // (endTime - startTime)

    def frameRateLimit(self, startTime):
        curTime = pygame.time.get_ticks()
        timeInLoop = curTime - startTime
        if timeInLoop < self.targetFrame:
            pygame.time.delay(self.targetFrame - timeInLoop)


if __name__ == '__main__':
    drone = DroneMaster()
    drone.go()
