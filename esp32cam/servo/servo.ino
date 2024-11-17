#include <ESP32Servo.h>

Servo ServoInorganic;  // create servo object to control a servo
Servo ServoOrganic;  // create servo object to control a servo

// 16 servo objects can be created on the ESP32

int pos = 0;    // variable to store the servo position
int pos2 = 0;
// Recommended PWM GPIO pins on the ESP32 include 2,4,12-19,21-23,25-27,32-33 
int ServoPinInorganic = 18;
int ServoPinOrganic = 19;
const int trigPin = 23;
const int echoPin = 22;

//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration;
float distanceCm;
float distanceInch;



void setup() {
  Serial.begin(115200);
  while (!Serial) {
        ; // Wait for serial port to connect. Needed for native USB
  }
  ServoInorganic.attach(ServoPinInorganic, 500, 2400); // attaches the servo on pin 18 to the servo object
  ServoOrganic.attach(ServoPinOrganic, 500, 2400);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  // using default min/max of 1000us and 2000us
  // different servos may require different min/max settings
  // for an accurate 0 to 180 sweep
}

void loop() {
  /*
  */
  while(Serial.available()){
    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
  
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
  
    // Calculate the distance
    distanceCm = duration * SOUND_SPEED/2;

    Serial.println(distanceCm);
  
    // Convert to inches
    distanceInch = distanceCm * CM_TO_INCH;
   
    char received = Serial.read();
    switch (received) {
      case '0': 
        Serial.println("State 0: 00");
        for (pos = pos; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
          ServoInorganic.write(pos);    // tell servo to go to position in variable 'pos'
          delay(15);              // waits 15ms for the servo to reach the position
        }
        for (pos2 = pos2; pos2 >= 0; pos2 -= 1) { // goes from 180 degrees to 0 degrees
          ServoOrganic.write(pos2);    // tell servo to go to position in variable 'pos'
          delay(15);              // waits 15ms for the servo to reach the position
        }
        break;
      case '1': 
        Serial.println("State 1: 01");
        for (pos = pos; pos <= 155; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
          ServoInorganic.write(pos);    // tell servo to go to position in variable 'pos'
          delay(15);             // waits 15ms for the servo to reach the position
        }
        for (pos2 = pos2; pos2 >= 0; pos2 -= 1) { // goes from 180 degrees to 0 degrees
          ServoOrganic.write(pos2);    // tell servo to go to position in variable 'pos'
          delay(15);              // waits 15ms for the servo to reach the position
        }
        break;
      case '2': 
        Serial.println("State 2: 10");
        for (pos2 = pos2; pos2 <= 155; pos2 += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
          ServoOrganic.write(pos2);    // tell servo to go to position in variable 'pos'
          delay(15);             // waits 15ms for the servo to reach the position
        }
        for (pos = pos; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
          ServoInorganic.write(pos);    // tell servo to go to position in variable 'pos'
          delay(15);              // waits 15ms for the servo to reach the position
        }
        
        break;
      case '3': 
        Serial.println("State 3: 11");
        break;
      default:
        Serial.println("Invalid state");
        break;
    }
  }
}
