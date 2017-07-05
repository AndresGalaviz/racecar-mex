#!/usr/bin/env python

import rospy
import numpy as np
from std_msgs.msg import String, Header
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from sensor_msgs.msg import LaserScan

KP = 0.3
TARGET_DISTANCE = 3.0
SPEED = .5

class WallFollow():
    def __init__(self):
        self.pub = rospy.Publisher("/vesc/ackermann_cmd_mux/input/teleop", AckermannDriveStamped, queue_size =1 )
        rospy.Subscriber("/scan",LaserScan, self.reading, queue_size = 1)

    def control(self, RD):
        pub = rospy.Publisher("/vesc/ackermann_cmd_mux/input/teleop", AckermannDriveStamped, queue_size =1 )

        Error = TARGET_DISTANCE - RD
        Target_angle = Error * KP

        drive_msg_stamped = AckermannDriveStamped()
        drive_msg = AckermannDrive()
        drive_msg.speed = SPEED
        drive_msg.steering_angle = Target_angle
        drive_msg_stamped.drive = drive_msg
        self.pub.publish(drive_msg_stamped)
        
    def reading(self, msg):
        #print msg.ranges

        max_a = msg.angle_max
        min_a = msg.angle_min
        a_inc = msg.angle_increment

        Right_distance = msg.ranges[int((-np.pi/2 + max_a)/a_inc)]
        #Right_distance = msg.ranges[int((-np.pi/2 + max_a)/a_inc)]

        self.control(Right_distance)
        #print msg.ranges[Left_distance] , msg.ranges[Right_distance]



if __name__=="__main__":
    rospy.init_node("wall_follow")
    WallFollow()
    rospy.spin()