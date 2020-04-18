#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

Turtle_pub = rospy.Publisher('Main_Sub', String, queue_size=30)
FLAG = 0

def callback(data):
    global Turtle_pub
    global FLAG
    rate = rospy.Rate(10)
    if data.data == "Turtle_start" and FLAG == 0:
        print('Turtle: I start to go to the people room')
        time.sleep(5)
        Turtle_reach_1_str = "Turtle_reach_1"
        Turtle_pub.publish(Turtle_reach_1_str)
        FLAG = 1

    if data.data == "Turtle_go" and FLAG == 1:
        print('Turtle: I am ready to find goods')
        time.sleep(5)
        Turtle_reach_2_str = "Turtle_reach_2"
        Turtle_pub.publish(Turtle_reach_2_str)
        FLAG = 2

    if data.data == "Turtle_back" and FLAG == 2:
        print('Turtle: I ready to go back to the people room')
        time.sleep(5)
        Turtle_reach_3_str = "Turtle_reach_3"
        Turtle_pub.publish(Turtle_reach_3_str)
        FLAG = 3
    rate.sleep()


if __name__ =='__main__':
    try:
        rospy.init_node('Simulation_py', anonymous=True)
        rospy.Subscriber("Main_Pub", String, callback)
        rospy.spin()
    except rospy.ROSInitException:
        pass