import threading
import time
import cv2
import socket
import bluetooth
import network

print(bluetooth.discover_devices(lookup_names=True))
bt = network.BluetoothControlClient()
bt.tryConnect()

print(bt.cmdRecv())
bt.cmdSend(1)
print(bt.cmdRecv())
