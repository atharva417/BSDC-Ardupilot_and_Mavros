# Import mavutil
from pymavlink import mavutil, mavwp
import time
# Create the connection
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()
# Set mode to takeoff
master.set_mode_apm("TAKEOFF")
# Arm
master.arducopter_arm()
# Wait for 3 sec
time.sleep(3)
# Initialise wp as object
wp = mavwp.MAVWPLoader()
# Now load waypoint.txt file.
wp.load("/home/atharva/ardupilot/ArduPlane/waypoint2.txt")
master.waypoint_clear_all_send()
master.waypoint_count_send(wp.count())
# Now send waypoints in files one by one
for i in range(wp.count()):
    msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)
    master.mav.send(wp.wp(msg.seq))
    print 'Sending waypoint {0}'.format(msg.seq)
# Finally set it to auto mode.
master.set_mode_apm("AUTO")
