import rospy
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode

rospy.wait_for_service('/mavros/cmd/arming')
try:
    arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    response = arming(1)
    response.success
#    arming.call(0)
except rospy.ServiceException, e:
    print "Service call failed: %s"%e