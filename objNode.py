#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from object.detector import Detector
import sys
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except ValueError:
    pass
import cv2


class RosObjDetector(object):
    def __init__(self, save_path):
        self.detector = Detector(save_path=save_path)
        self.pub = rospy.Publisher('obj_pub', String, queue_size=10)
        rospy.init_node('obj_pub', anonymous=False)

    def callback(self, data):
        print("Here is callback")
        if data.data == "object_reached":
            cam_id = 'http://192.168.3.66:4747/video'
            detected_frame = self.detector.detect_cam(cam_id)
            cv2.imwrite("ObjScene.jpg", detected_frame)
            if not rospy.is_shutdown():
                done_msg = "object_detected"
                rospy.loginfo(done_msg)
                self.pub.publish(done_msg)

    def listen(self):
        # rospy.init_node('listener', anonymous=True)
        print("waiting for message")
        rospy.Subscriber("main_pub", String, self.callback)
        print('After sub')
        rospy.spin()


if __name__ == '__main__':
    objDetector = RosObjDetector(save_path='objectFound')
    objDetector.listen()
    print('After listen')
