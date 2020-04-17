import rospy
from std_msgs.msg import String
import sys
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except ValueError:
    pass
import os
import time
from utils import SocketServer

faces = []  # face image file name list
requests = []  # request text file name list

module_path = os.path.dirname(__file__)

receive_path = 'requestGot'

def callback(data):
    if data.data == 'send_object':
        to_send_files = []
        found_path = 'objectFound'
        for root, _, files in os.walk(receive_path):
            for file in files:
                if file.split('.')[-1] == 'txt':
                    with open(os.path.join(root, file), 'r') as rf:
                        lines = rf.readlines()
                    for line in lines:
                        request = line.strip().split(' ')[-1]
                        obj_filename = request + '.jpg'
                        to_send_files.append(os.path.join(found_path, obj_filename))
        num_to_sent = len(to_send_files)
        num_name = str(num_to_sent) + '.txt'
        with open(num_name, 'w') as wf:
            wf.write(str(num_to_sent))
        sent = server.sendFile(num_name)
        time.sleep(1)
        if not sent:
            print(num_name + ' failed to send.')
        for file in to_send_files:
            sent = server.sendFile(file)
            time.sleep(1)
            if not sent:
                print(file + ' failed to send.')
        print(str(num_to_sent) + ' files have been sent to client.')


server = SocketServer()
pub = rospy.Publisher('tcp_pub', String, queue_size=10)
rospy.init_node('tcp_pub', anonymous=False)
rospy.Subscriber("main_pub", String, callback)
server.waitConnection()


while True:
    received, fn = server.receiveFile(receive_path)
    if received:
        if fn.split('.')[-1] == 'txt':
            requests.append(fn)
        elif fn.split('.')[-1] == 'jpg' or fn.split('.')[-1] == 'png':
            faces.append(fn)
            name = fn.split('.')[0]
            rospy.loginfo(name)
            pub.publish(name)




