#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

t = Twist()

def my_name():
    print('Start')
    for x in range(20):
        t.linear.x = 0.5
        t.linear.y = 0
        t.angular.z = 0
        pub.publish(t)
        rate.sleep()
    for x in range(37):
        t.linear.x = 0
        t.linear.y = 0
        t.angular.z = 0.5
        pub.publish(t)
        rate.sleep()
    for x in range(12):
        t.linear.x = 0.5
        t.linear.y = 0
        t.angular.z = 0
        pub.publish(t)
        rate.sleep()

def Name():
    global pub, rate
    rospy.init_node('Name', anonymous=True)
    rate = rospy.Rate(10) # 10hz 
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    my_name()
    rospy.spin()

if __name__ == '__main__':
    try:
        Name()
    except rospy.ROSInterruptException:
        pass
