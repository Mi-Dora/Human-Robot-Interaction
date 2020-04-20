#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
import time
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from utils import broadcast

pub = rospy.Publisher('Main_Pub', String, queue_size=30)
COUNT = 0


def Main_callback(data):
    # rate = rospy.Rate(10)
    global pub
    msg = ''
    print("Here is Main_callback.")
    if data.data == "Turtle_reach_human1":     # Once turtle reaches the people room, start face&mic
        print('Turtle has reached the people room, start the face&mic')
        broadcast("龟龟已到达房间，开始寻找客人。")
        msg = "Human_detect"

    elif data.data == "Human1":     # The first human has been detected, find the second one
        print('Turtle has found the first guest.')
        broadcast("已找到第一位客人，正在寻找第二位客人。")
        msg = "Human_find2"

    elif data.data == "Human2":     # The second human has been detected, find the third one
        print('Turtle has found the second guest.')
        broadcast("已找到第二位客人，正在寻找第三位客人。")
        msg = "Human_find3"

    elif data.data == "Human3":   # Face&mic finish, Turtle finds goods
        print('Face&mic finish, Turtle ready to find goods')
        broadcast("已找到三位客人，出发去取客人需要的物品。")
        msg = "Turtle_go"

    elif data.data == "Turtle_reach_goods":   # Once turtle reaches the goods room, start object detect
        print('Turtle reached the goods room, start object detect')
        broadcast("龟龟已到达，开始寻找需要的物品。")
        msg = "Object_detect"

    elif data.data == "Object_detected":  # Object detect finish, Turtle goes back to the people room
        print('Object detect finish, Turtle goes back to the people room')
        broadcast("已找到物品，龟龟将返回送给客人。")
        msg = "Turtle_back"

    elif data.data == "Turtle_reach_human2":   # Send message to TCP Server for call face&mic
        print('Turtle already gone back to the people room, start the Human compare')
        broadcast("龟龟已回到客人的房间，开始分发物品。")
        msg = "Send_object"

    pub.publish(msg)
    # rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('Main_py', anonymous=False)

        start_str = "Turtle_start"
        broadcast("龟龟启动，出发去客人房间。")
        pub.publish(start_str)

        rospy.Subscriber("Main_Sub", String, Main_callback)
        rospy.spin()
    except rospy.ROSInitException:
        pass
