/*
Project file for controlling the gait-algorithm of the Y-robot for Bio inspired robotics project

Using board [Arduino UNO R3]
With shield [TA0039 Sensor Expansion Shield V5.0] (https://makerhero.com/img/files/download/TA0039-Datasheet.pdf)
To control servo [Fitec FS90 9G Mini Servo] (https://www.addicore.com/products/feetech-fitec-fs90-9g-mini-servo-with-accessories)

Servo has cables:
Brown    = Ground
Red      = Power
Yellow   = Signal

Servo can have pins >= 2, since 0 and 1 are interfered with by Serial connection.

This file takes a gait description vector and creates a series of motor inputs for the arduino
*/

#include <iostream>
#include <vector>

struct motorCMD{
  int motorID;
  float t_start;
  float dt;
};




int main(int argc, char* argv[]){

    

    return 1;
}