# BSDC-Ardupilot_and_Mavros
The mavros_msgs package is taken as it is from mavros. It contains all required msg and srv files.
The mavros_py package includes launch, scripts, waypointfiles folders.

The launch folder contains apm.launch, which is used to launch mavros topics and services. Note that this apm.launch is edited accordingly so that it can connect with ardupilot sitl, as mentioned in docs (FCU ID).

The scripts folder contains the python scripts of which mavarm, mavmode, mavtakeoff are subsidiary files. mavmission.py is main file which coordinates whole mission from start to end.

The scripts folder also contains the pymavlink folder containing python files which use the pymavlink package to coordinate the  mission.

## Order of execution of files:
1.  sim_vehicle.py -v ArduPlane --console --map (In Terminal 1)
2.  (Wait for the map to open.)
3.  (source the workspace (In Terminal 2))
4.  Roslaunch mavros apm.launch (In Terminal 2)
5.  (source the workspace (In Terminal 3)
6.  rosrun mavros (name of whichever mission py file to be run here)

In Step 6 above, the py file to be run can be different, and depends on the method chosen (pymavlink or Mavros)

## For PyMavlink
There are two important files here mission.py and dynamicwp.py. First run mission.py which uses waypoint file waypoint2.txt. Then in the middle of the ongoing mission run dynamicwp.py file which uses waypoint3.txt. Thus plane pauses current ongoing mission and starts new mission, complete it  first and then resume original mission. (In Step 6 of the Above)

## For Mavros
Use the mavmission.py file in Step 6 above

# Pymavlink Installation
This is a python implementation of the MAVLink protocol.
It includes a source code generator (generator/mavgen.py) to create MAVLink protocol implementations for other programming languages as well.
Also contains tools for analizing flight logs.

## Documentation

Please see http://ardupilot.org/dev/docs/mavlink-commands.html for documentation.

For realtime discussion please see the pymavlink gitter channel here
https://gitter.im/ArduPilot/pymavlink


## Installation 

Pymavlink supports both python2 and python3.

The following instructions assume you are using Python 2 and a Debian-based (like Ubuntu) installation.

## Dependencies

Pymavlink has several dependencies :

    - future : for python 2 and python 3 interoperability (http://python-future.org/)
    - lxml : for checking and parsing xml file (http://lxml.de/installation.html)
    - python-dev : for mavnative
    - a C compiler : for mavnative

Optional :

    - numpy : for FFT
    - pytest : for tests

### On linux

lxml has some additional dependencies that can be installed with your package manager (here with `apt-get`) :

```bash
sudo apt-get install gcc python-dev libxml2-dev libxslt-dev
```

Optional for FFT scripts and tests:

```bash
sudo apt-get install python-numpy python-pytest
```

Using pip you can install the required dependencies for pymavlink :

```bash
sudo pip2 install -U future lxml
```

The -U parameter allows updating future and lxml version if it is already installed.

### On Windows

Use pip to install future as for linux.
Lxml can be installed with a windows installer from here : https://pypi.python.org/pypi/lxml/3.6.0


## Installation

### For users

It is recommended to install pymavlink from PyPi with pip, that way dependencies should be auto install by pip.

```bash
sudo pip2 install -U pymavlink
```

The -U parameter allow to update pymavlink version if it is already installed.

#### Mavnative

By default, pymavlink will try to compile and install mavnative which is a C extension for parsing mavlink. Mavnative only supports mavlink1.
To skip mavnative installation and reduce dependencies like `gcc` and `python-dev`, you can pass `DISABLE_MAVNATIVE=True` environment variable to the installation command:

```bash
sudo DISABLE_MAVNATIVE=True pip2 install -U pymavlink
```

### For developers

On the pymavlink directory, you can use :

```bash
sudo MDEF=PATH_TO_message_definitions pip2 install . -v
```

The -v parameter will output the installation commands on the terminal.
The MDEF usage is require as pip install is done from /tmp directory, so it is necessary to use MDEF variable to 
point on the message_definitions directory.
Use pip should auto install dependencies and allow to keep them up-to-date with pip. 

Or:

```bash
sudo python2 setup.py install
```
