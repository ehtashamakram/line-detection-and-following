#!/usr/bin/env python
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
def image_callback(msg):
	bridge = cv_bridge.CvBridge()
	cv2.namedWindow("window", 1)
	twist = Twist()
	image = bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')   
    #### 1.GET IMAGE INFO AND CROP ####
	h, w, d = image.shape
	descentre = 160
	rows_to_watch = 100
	crop_img = image[(h)/2+descentre: (h)/2+(descentre+rows_to_watch)][1:w]
		
		#### 2.GET IMAGE INFO AND CROP ####
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	lower_yellow = numpy.array([ 20, 100, 100])
	upper_yellow = numpy.array([30, 250, 250])

		#### 3.APPLY THE MASK ####
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	res = cv2.bitwise_and(image,image,mask= mask)
		
		#### 4.GET THE CENTROIDS, DRAW A CIRCLE ####
		#search_top = 3*h/4
		#search_bot = search_top + 80
		#mask[0:search_top, 0:w] = 0
		#mask[search_bot:h, 0:w] = 0
	M = cv2.moments(mask, False)
		#if M['m00'] > 0:
	try:
		#	print "M['m00'] = " + str(int(M['m00']))
		#	print "M['m10'] = " + str(int(M['m10']))
		#	print "M['m01'] = " + str(int(M['m01']))
		#	print "w = " + str(w)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		#	print "cx = " + str(int(cx))
		#	print "cy = " + str(int(cy))
	except ZeroDivisionError:
		cx = w/2
		cy = h/2

	cv2.circle(res, (cx, cy), 10, (0,0,255), -1)

	err = cx - w/2
			#print "err = " + str(int(err/500))
	twist.linear.x = 0.1
	print twist.linear.x
	twist.angular.z = -float(err) / 500
	print twist.linear.z
	cmd_vel_pub.publish(twist)
	cv2.imshow("window", image)
	cv2.imshow("Mask", res)
	cv2.waitKey(1)

rospy.init_node('follower')
image_sub = rospy.Subscriber('/camera/image', Image, image_callback)
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
rospy.spin()
