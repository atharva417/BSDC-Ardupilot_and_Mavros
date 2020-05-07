# BSDC-Ardupilot_and_Mavros
mavros_msgs package is taken as it is from mavros. It contains all required msg and srv files.
mavros_py package includes launch, scripts, waypointfiles folders.

launch contains apm.launch, which is used to launch mavros topics and services. Note that this apm.launch is edited accordingly so that it can connect with ardupilot sitl, as mentioned in docs.

scripts contains python scripts of which mavarm, mavmode, mavtakeoff are subsidiary files. mavmission.py is main file which coordinates whole mission from start to end.

scripts also contains pymavlink folder containing python files which use pymavlink package to coordinate mission.
There are two important files here mission.py and dynamicwp.py. First run mission.py which uses waypoint file waypoint2.txt. Then in the middle of ongoing mission run dynamicwp.py file which uses waypoint3.txt. Thus plane pauses current ongoing mission and starts new mission, complete it  first and then resume original mission.
