/*
Project for controlling servo using Arduino board for Bio inspired robotics project

Using board [Arduino UNO R3]
With shield [TA0039 Sensor Expansion Shield V5.0] (https://makerhero.com/img/files/download/TA0039-Datasheet.pdf)
To control servo [Fitec FS90 9G Mini Servo] (https://www.addicore.com/products/feetech-fitec-fs90-9g-mini-servo-with-accessories)

Servo has cables:
Brown    = Ground
Red      = Power
Yellow   = Signal

Servo can have pins >= 2, since 0 and 1 are interfered with by Serial connection.
*/

#include <Servo.h> 
Servo myservo;  // create servo object to control a servo 

void setup() {
    Serial.begin(115200);
    myservo.write(0); // Initial servo angle
    myservo.attach(2);  // Servo pin
    Serial.println("ManualControl started!");
}

void loop() {
    String readString;
    
    // Get data from serial port
    while (Serial.available()) {
        char c = Serial.read();  // Get one byte from serial buffer
        readString += c; // Make the string readString
        delay(2);  // Slow dowm looping to allow buffer to fill with next character
    }

    // Handle data
    if (readString.length() > 0) {
        // Write back a copy of what was recieved
        Serial.println(readString);
        int n = readString.toInt();

        // Write position to servo
        Serial.print("Angle: ");
        Serial.println(n);
        myservo.write(n);
    } 
}