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
    if data.data == "Turtle_reach_1":     # Once turtle reaches the people room, start face&mic
        print('Turtle reached the people room, start the face&mic')
        Human_detect_str = "Human_detect"
        pub.publish(Human_detect_str)
    elif data.data == "Human_detected":   # Face&mic finish, Turtle finds goods
        print('Face&mic finish, Turtle ready to find goods')
        Turtle_go_str = "Turtle_go"
        pub.publish(Turtle_go_str)
    elif data.data == "Turtle_reach_2":   # Once turtle reaches the goods room, start object detect
        print('Turtle reached the goods room, start object detect')
        Object_detect_str = "Object_detect"
        pub.publish(Object_detect_str)
    elif data.data == "Object_detected":  # Object detect finish, Turtle goes back to the people room
        print('Object detect finish, Turtle goes back to the people room')
        Turtle_back_str = "Turtle_back"
        pub.publish(Turtle_back_str)
    elif data.data == "Turtle_reach_3":   # Object detect finish, Turtle goes back to the people room
        print('Turtle already gone back to the people room, start the Human compare')
        Human_compare_str = "Human_compare"
        pub.publish(Human_compare_str)
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