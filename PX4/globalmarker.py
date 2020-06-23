import sys
from pylab import *
import numpy as np
import time
from matplotlib import pyplot as plt
import cv2
from cv_bridge import CvBridge
import rospy
from sensor_msgs.msg import *
from std_msgs.msg import *
import tf, geometry_msgs, tf2_ros
from geometry_msgs.msg import PointStamped, PoseStamped
#from tf import TransformBroadcaster

def height(msg):
	global h
	h = msg.pose.position.z

def callback(data):
	global k
	k = data.K

def detect(data):
	global k, h
	b = np.array([[k[0], k[1], k[2]], [k[3], k[4], k[5]], [k[6], k[7], k[8]]])
	bridge = CvBridge()
	cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
	imgray = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
	kernel = np.ones((5,5),np.uint8)
	dilation = cv2.dilate(imgray,kernel,iterations = 1)
	ret,thresh = cv2.threshold(dilation,127,255,0)
	_, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	if(len(contours)!=0):
		print('marker found')
		for cnt in contours:
			epsilon = 0.1*cv2.arcLength(cnt,True)
			approx = cv2.approxPolyDP(cnt,epsilon,True)
			if (len(approx) == 4):
				cv2.drawContours(cv_image, [approx], 0, (255,30,20), 6)
				M = cv2.moments(cnt)
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				f = 554.382713
				ipp = np.array([[cx],[cy],[1]]) # 2d target coord 
				invk = np.linalg.inv(b)
				rf = np.array([[0, 0, f], [-f, 0, 0], [0, -f, 0]]) # focal lenght matrix
				invf = np.dot(rf, invk)
				ipt = np.dot(invf,ipp) # 3d image plane target cood
				(trans,rot) = lisn.lookupTransform("/world", "fpv_link", rospy.Time(0))
				euler = tf.transformations.euler_from_quaternion(rot)
				rm = tf.transformations.euler_matrix(euler[0],euler[1],euler[2])
				wfrm = [[rm[0][0],rm[0][1],rm[0][2]],[rm[1][0],rm[1][1],rm[1][2]],[rm[2][0],rm[2][1],rm[2][2]]] # Transformation matrix for world frame
				detipt = sqrt(ipt[0]**2 + ipt[1]**2 + ipt[2]**2) # magnitude of ipt
				uipt = ipt/detipt
				ls = np.array(np.dot(wfrm,uipt))
				lr = np.array([0,0,-1])
				cos = np.dot(lr,ls)
				d = h/cos
				cord = d*(uipt) # 3d target coord in camera frame
				print(cord, 'in cam frame')
				ps = PointStamped()
				ps.header.frame_id = "fpv_link"
				ps.header.stamp = rospy.Time(0)
				ps.point.x = cord[0]
				ps.point.y = cord[1]
				ps.point.z = cord[2]
				mat = listener.transformPoint("/world", ps)
				rospy.loginfo(mat)

			cv2.imshow('frame',cv_image)
			k = cv2.waitKey(5) & 0xFF
	else:
		print('no marker detected')
		cv2.imshow('frame',cv_image)
		k = cv2.waitKey(5) & 0xFF

if __name__ == '__main__':
	k = []
	p = []
	rospy.init_node('image_gazebo', anonymous=True)
	listener = tf.TransformListener()
	lisn = tf.TransformListener()
	rospy.Subscriber("/plane_cam/usb_cam/camera_info", CameraInfo, callback)
	rospy.Subscriber("/mavros/local_position/pose", PoseStamped, height)
	time.sleep(2)
	rospy.Subscriber("/plane_cam/usb_cam/image_raw", Image, detect)
	rospy.spin()




'''
	k[0][0] = a[0][0]
	k[0][1] = a[0][1]
	k[0][2] = a[0][2]
	k[1][0] = a[0][3]
	k[1][1] = a[0][4]
	k[1][2] = a[0][5]
	k[2][0] = a[0][6]
	k[2][1] = a[0][7]
	k[2][2] = a[0][8]
	p[0][0] = b[0][0]
	p[0][1] = b[0][1]
	p[0][2] = b[0][2]
	p[1][0] = b[0][4]
	p[1][1] = b[0][5]
	p[1][2] = b[0][6]
	p[2][0] = b[0][8]
	p[2][1] = b[0][9]
	p[2][2] = b[0][10]
'''