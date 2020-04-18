#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

pub = rospy.Publisher('Main_Pub', String, queue_size=30)
COUNT = 0


def Main_callback(data):
    rate = rospy.Rate(10)
    global pub
    msg = ''
    if data.data == "Turtle_reach_human1":     # Once turtle reaches the people room, start face&mic
        print('Turtle reached the people room, start the face&mic')
        msg = "Human_detect"

    elif data.data == "Human1":     # The first human has been detected, find the second one
        print('Turtle reached the people room, start the face&mic')
        msg = "Human_Find2"

    elif data.data == "Human2":     # The second human has been detected, find the third one
        print('Turtle reached the people room, start the face&mic')
        msg = "Human_Find3"

    elif data.data == "Human3":   # Face&mic finish, Turtle finds goods
        print('Face&mic finish, Turtle ready to find goods')
        msg = "Turtle_go"

    elif data.data == "Turtle_reach_goods":   # Once turtle reaches the goods room, start object detect
        print('Turtle reached the goods room, start object detect')
        msg = "Object_detect"

    elif data.data == "Object_detected":  # Object detect finish, Turtle goes back to the people room
        print('Object detect finish, Turtle goes back to the people room')
        msg = "Turtle_back"

    elif data.data == "Turtle_reach_human2":   # Send message to TCP Server for call face&mic
        print('Turtle already gone back to the people room, start the Human compare')
        msg = "Send_Object"

    pub.publish(msg)
    rate.sleep()


if __name__ =='__main__':
    try:
        rospy.init_node('Main_py', anonymous=True)

        start_str = "Turtle_start"
        pub.publish(start_str)

        rospy.Subscriber("Main_Sub", String, Main_callback)
        rospy.spin()
    except rospy.ROSInitException:
        pass
