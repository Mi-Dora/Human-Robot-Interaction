#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time

pub = rospy.Publisher('Main_Sub', String, queue_size=30)
FLAG = 0

def Face_callback(data):
    global pub
    global FLAG
    rate = rospy.Rate(10)
    if data.data == "Human_detect" and FLAG == 0:
        print('Human_detect start')
        time.sleep(5)
        Human_detected_str = "Human_detected"
        pub.publish(Human_detected_str)
        FLAG = 1

    if data.data == "Human_compare" and FLAG == 1:
        print('Start to compare')
        FLAG = 2
        print("Game Over")

    rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('Face_mic_py', anonymous=True)
        rospy.Subscriber("Main_Pub", String, Face_callback)
        rospy.spin()
    except rospy.ROSInitException:
        pass