import rospy
from std_msgs.msg import String
import sys
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except ValueError:
    pass
import socket
import os
import sys
import struct
from utils import SocketServer

num_people = 3

server = SocketServer()
pub = rospy.Publisher('tcp_pub', String, queue_size=10)
server.waitConnection()
server.sendFile('../UHD.png')
while True:
    # server.receiveMessage()
    server.receiveFile('serverSaved')



