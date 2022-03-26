import struct
import numpy as np
import network
import utils
import cv2


NET_STAT_OK = '100'
NET_STAT_CONTINUE = '200'
config = utils.Config('./config.yaml')
net = network.NetworkServer(config)
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 5)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))


def exchange():
    ping = net.cmdRecv()
    net.cmdSend(ping)

    pack = net.packRecv()
    ctlX, ctlY = struct.unpack('ff', pack)
    net.cmdSend(NET_STAT_OK)

    ret = net.cmdRecv().rstrip()
    if ret != NET_STAT_CONTINUE:
        print('???NET_STAT_CONTINUE')

    videoArray = cam.read()[1]
    videoArray = cv2.resize(videoArray, (640, 480))
    videoEncoded = cv2.imencode('.jpg', videoArray)
    videoEncoded = np.array(videoEncoded[1])
    videoData = videoEncoded.tobytes()
    videoSize = len(videoData)
    net.cmdSend(videoSize)

    ret = net.cmdRecv().rstrip()
    if ret != NET_STAT_OK:
        print('???NET_STAT_OK')
    net.dataSend(videoData)


net.tryConnect()
while True:
    exchange()
