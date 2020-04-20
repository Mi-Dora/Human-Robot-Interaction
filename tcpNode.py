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
found_path = 'objectFound'
facemic_start = False
# object_sent = False


def multi_send(receive_path, found_path):
    global server
    to_send_files = []

    for root, _, files in os.walk(receive_path):
        for file in files:
            if file.split('.')[-1] == 'txt':
                with open(os.path.join(root, file), 'r') as rf:
                    lines = rf.readlines()
                for line in lines:
                    request = line.strip().split('\t')[-1]
                    obj_filename = request + '.jpg'
                    if os.path.exists(os.path.join(found_path, obj_filename)):
                        to_send_files.append(os.path.join(found_path, obj_filename))
    num_to_sent = len(to_send_files)
    num_name = str(num_to_sent) + '.txt'
    with open(num_name, 'w') as wf:
        wf.write(str(num_to_sent))
    sent = server.sendFile(num_name)
    server.waitConnection()
    # time.sleep(1)
    if not sent:
        print(num_name + ' failed to send.')
    for file in to_send_files:
        sent = server.sendFile(file)
        server.waitConnection()
        # time.sleep(1)
        if not sent:
            print(file + ' failed to send.')
    print(str(num_to_sent) + ' files have been sent to client.')


def callback(data):
    global facemic_start
    if data.data == 'Human_detect':
        message = 'Human_detect.txt'
        with open(message, 'w') as wf:
            wf.write(message.split('.')[0])
        sent = server.sendFile(message)
        server.waitConnection()
        # if sent:
        #     facemic_start = True
        time.sleep(1)
    elif data.data == 'Send_object':
        multi_send(receive_path, found_path)


server = SocketServer()
pub = rospy.Publisher('Main_Sub', String, queue_size=10)
rospy.init_node('Tcp_py', anonymous=False)
rospy.Subscriber("Main_Pub", String, callback)
server.waitConnection()

received_num = 0
human_num = 0
while True:
    # if not facemic_start:
    #     continue
    received, fn = server.receiveFile(receive_path)
    if received:

        if fn.split('.')[-1] == 'txt':
            requests.append(fn)
        elif fn.split('.')[-1] == 'jpg' or fn.split('.')[-1] == 'png':
            faces.append(fn)
            human_num += 1
            name = fn.split('.')[0]
            msg = 'Human' + str(human_num)
            rospy.loginfo(name + ' found')
            pub.publish(msg)
        received_num += 1
        server.waitConnection()
        # if received_num == 4:
        #     break
# rospy.spin()



