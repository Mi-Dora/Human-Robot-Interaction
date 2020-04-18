#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time

Object_pub = rospy.Publisher('Main_Sub', String, queue_size=30)
FLAG = 0

def Object_callback(data):
    global Object_pub
    global FLAG
    rate = rospy.Rate(10)

    if data.data == "Object_detect" and FLAG == 0:
        print('Object_detect start')
        time.sleep(5)
        Object_detected_str = "Object_detected"
        Object_pub.publish(Object_detected_str)
        FLAG = 1
    rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('Object_py', anonymous=True)
        rospy.Subscriber("Main_Pub", String, Object_callback)
        rospy.spin()
    except rospy.ROSInitException:
        pass