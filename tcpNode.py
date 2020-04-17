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

num_to_receive = num_people * 2

faces = []  # face image file name list
requests = []  # request text file name list

module_path = os.path.dirname(__file__)


def callback(data):
    if data.data == 'send_object':
        foundPath = module_path + 'objectFound'
        for root, _ , files in os.walk(foundPath):
            for file in files:
                sent = server.sendFile(os.path.join(root, file))
                if sent:
                        pass



server = SocketServer()
pub = rospy.Publisher('tcp_pub', String, queue_size=10)
rospy.init_node('tcp_pub', anonymous=False)
rospy.Subscriber("main_pub", String, callback)
server.waitConnection()
# server.sendFile('../UHD.png')

while True:
    received, fn = server.receiveFile('requestGot')
    if received:
        if fn.split('.')[-1] == 'txt':
            requests.append(fn)
        elif fn.split('.')[-1] == 'jpg' or fn.split('.')[-1] == 'png':
            faces.append(fn)
            name = fn.split('.')[0]
            rospy.loginfo(name)
            pub.publish(name)
    for face in faces:
        name = face.split('.')[0]
        request = name + '.txt'
        if request in requests:
            rospy.loginfo(name)
            pub.publish(name)
            faces.remove(face)
            requests.remove(request)
            break



