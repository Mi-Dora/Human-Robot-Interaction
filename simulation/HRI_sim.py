import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import UInt16
from math import radians

#flag = 0;

class GoToPose():
    def __init__(self):

        self.goal_sent = False

	# What to do if shut down (e.g. Ctrl-C or failure)
	rospy.on_shutdown(self.shutdown)
	
	# Tell the action client that we want to spin a thread by default
	self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
	rospy.loginfo("Wait for the action server to come up")

	# Allow up to 5 seconds for the action server to come up
	self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

	# Start moving
        self.move_base.send_goal(goal)

	# Allow TurtleBot up to 60 seconds to complete task
	success = self.move_base.wait_for_result(rospy.Duration(60)) 

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)
def adjustcallback(data):
        cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
	    # 5 HZ
        r = rospy.Rate(5);

        angle = 5*int(data.data/5)
        #let's turn at 5 deg/s
        turn_cmd = Twist()
        turn_cmd.linear.x = 0
        turn_cmd.angular.z = radians(5); #1 deg/s in radians/s

        rospy.loginfo("Turning")
        for x in range(0,angle):
            cmd_vel.publish(turn_cmd)
            r.sleep()   
        rospy.loginfo("finish")
        talker(7)
        return

def callback(data):
    if data.data == 0:
        navigator = GoToPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': 1.00, 'y' : -2.37}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Reached the guest room")
            talker(4)
        else:
            rospy.loginfo("The base failed to reach!")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
    elif data.data == 1:
        navigator = GoToPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': -0.45, 'y' : -2.39}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Reached the thing room")
            talker(5)
        else:
            rospy.loginfo("The base failed to reach!")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
    elif data.data == 2:
        navigator = GoToPose()

        # Customize the following values so they are appropriate for your location
        position = {'x': 1.00, 'y' : -2.37}
        quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

        rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Reached the guest room")
            talker(6)
        else:
            rospy.loginfo("The base failed to reach!")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)
    elif data.data == 3:
        try:
            #rospy.loginfo("Success to adjust the position!")
            AdjustPosition()
            #rospy.loginfo("come in adjust")
            #rospy.Subscriber("adjust_angle", UInt16,adjustcallback)
            #rospy.spin()
            #talker(7)
        except:
            rospy.loginfo("Failed to adjust the positon!")

def talker(sim_flag):
    pub = rospy.Publisher('turtle_sim_situation', UInt16, queue_size=10)
    #rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5) # 10hz
    for i in range(1):
        print("the situation of Turtlebot:\n \
            case 4:first time success to guest room \n \
            case 5: first time success to thing room \n \
            case 6: second time success o guest room \n \
            case 7: success to adjust the positon ")
        print(sim_flag)
        rospy.loginfo(sim_flag)
        pub.publish(sim_flag)
        rate.sleep()

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('HRI_sim', anonymous=True)

    sub = rospy.Subscriber("chatter", UInt16,callback)
    sub_1 = rospy.Subscriber("adjust_angle", UInt16,adjustcallback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")