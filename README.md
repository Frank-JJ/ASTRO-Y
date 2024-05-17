# Project for the absolute softest robotics.

This github contains the code for running and result from testing of the gait implementation on a Y-shaped soft robot.

To run a gait on the robot, code for recieving uart commands should be run on the arduino:
```
Arduino code\ManualControl\ManualControl.ino
```
At the same time code for sending uart commands should be run on a connected PC. This consists of a uart-sniffer, which allows data to be transmitted succesfully:
```
Arduino code\GaitControl\uartSniffer.py
```
And the actual gait control code:
```
Arduino code\GaitControl\gaitMachine.cpp
```
