# Import mavutil
from pymavlink import mavutil, mavwp
import time
# Create the connection
master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()
# Initialise wp as object
wp = mavwp.MAVWPLoader()
cout=3
# Now load waypoint.txt file.
wp.load("/home/atharva/ardupilot/ArduPlane/waypoint2.txt")

# Load 2nd wp file into a list.
file = open('/home/atharva/ardupilot/ArduPlane/waypoint3.txt', "r")
for line in file:
    if line.startswith('#'):
        comment = line[1:].lstrip()
        continue
    line = line.strip()
    if not line:
        continue
    a = line.split()
#    if len(a) != 12:
#        raise MAVWPError("invalid waypoint line with %u values" % len(a))
    if mavutil.mavlink10():
        fn = mavutil.mavlink.MAVLink_mission_item_message
    else:
        fn = mavutil.mavlink.MAVLink_waypoint_message
    w = fn(wp.target_system, wp.target_component,
           int(a[0]),    # seq
           int(a[2]),    # frame
           int(a[3]),    # command
           int(a[1]),    # current
           int(a[11]),   # autocontinue
           float(a[4]),  # param1,
           float(a[5]),  # param2,
           float(a[6]),  # param3
           float(a[7]),  # param4
           float(a[8]),  # x (latitude)
           float(a[9]),  # y (longitude)
           float(a[10])  # z (altitude)
           )
    if w.command == 0 and w.seq == 0 and wp.count() == 0:
        # special handling for Mission Planner created home wp
        w.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
    comment = ''    
    wp.insert(cout, w, comment)
    cout=cout+1
file.close()
wp.reindex()
#master.waypoint_clear_all_send()                                     
master.waypoint_count_send(wp.count())                          
# Now send waypoints in files one by one
for j in range(wp.count()):
    msg = master.recv_match(type=['MISSION_REQUEST'],blocking=True)             
    master.mav.send(wp.wp(msg.seq))                                                                      
    print 'Sending waypoint {0}'.format(msg.seq)  

master.set_mode_apm("AUTO")