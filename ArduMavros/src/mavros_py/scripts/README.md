The important files here are mavmission.py, mavmissionfile.py and mavmissiondyn.py which coordinates whole mission from start to end.
The mavmission.py send waypoints written in code itself.
The mavmissionfile.py send waypoints which are stored in a txt file.(here wayptmav.txt)
The mavmissiondyn.py file is used to send dynamic waypoints stored in a txt file.(here waypoint3.txt)
Follow the 'Order of Execution of Files' given in main readme of repo. 
There in 6th step first run mavmissionfile.py then when mission is in progress then run mavmissiondyn.py in other terminal.
Thus plane will start following new wps then after completing them it will continue original wp mission.
Here mavarm, mavmode, mavtakeoff are subsidiary files. 
In pymavlink folder we have mission.py and dynamicwp.py both of them use wps stored in txt file.
Run these files same as given above. mission.py first then dynamicwp.py in middle of ongoing mission.
Here arm.py is a subsidiary file.
