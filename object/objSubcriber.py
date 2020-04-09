#!/usr/bin/env python
# license removed for brevity
from speech.text2speech import synthesize_text
from speech.speechmain import speak
import linecache
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from object.detector import Detector
import base64
import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2


class RosObjDetector(object):
    def __init__(self):
        self.detector = Detector()
        rospy.init_node('Cimage_listener', anonymous=True)
        rospy.Subscriber("Camera_image", Image, self.callback)
        rospy.spin()

    def callback(self, data):
        bridge = CvBridge()
        try:
            cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
            detected = self.detector.detect(cv_image)
            if detected:
                pass
            else:
                pass
        except CvBridgeError as e:
            print(e)

    # def listener_py(self):
    #     rospy.init_node('Cimage_listener', anonymous=True)
    #     rospy.Subscriber("Camera_image", Image, self.callback)
    #     rospy.spin()


