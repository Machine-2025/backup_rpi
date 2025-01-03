// receiver boat servo 
// Libs
#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <ServoTimer2.h>

// Constants
const int nrf_CE_pin = 7;
const int nrf_CSN_pin = 8;
const int servo_pin = 3;
const int claw_pin = 2;
const byte address[6] = "00002";
const int servo_increment = 4;
const int servo_max_deg = 170;
const int servo_min_deg = 10;

// Variables
char robot_color = 'n'; // r ,g, b, y, o, p, null
                        // changer la couleur selon le robot avant de upload TODO
int pos_servo = 10;
int pos_claw = 10;

// Package struct
struct PackageNRF {
  int dir_left = 0;
  int dir_right = 0;
  char servo = 'a';
  char color = 'n';
  int claw = 15;
};

// Objects
PackageNRF package;
RF24 radio(nrf_CE_pin, nrf_CSN_pin);
ServoTimer2 servo;
ServoTimer2 claw;

// Function prototypes
int deg_to_pulse(int angle);
void writeServoAngle(int pin, int angle);
void dir_left_drive(int dir_left_in);
void dir_right_drive(int dir_right_in);
void servo_drive(char servo_direction);

// SETUP
void setup() {
  Serial.begin(9600);

  // NRF setup
  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  
  // Servo setup
  servo.attach(servo_pin);
  servo.write(deg_to_pulse(pos_servo));

  // Claw setup
  if (robot_color == 'n')
  {
    claw.attach(claw_pin);
    claw.write(deg_to_pulse(pos_claw));
  }
}

// LOOP
void loop() {

  // Receive NRF package
  if (radio.available())
  {
    radio.read(&package, sizeof(PackageNRF));
  }

  if(package.color != robot_color) // Package for other robot, back to default values
  {
    package.dir_left = 0;
    package.dir_right = 0;
    package.servo = 'a';
    package.claw = 10;
    pos_claw = 10;
    pos_servo = 10;
  }

  else // Package for this robot, read package values
  {
    servo_drive(package.servo);

    if (robot_color == 'n')
    {
      pos_claw = map(package.claw, 0, 1023, 35, 150);
      claw.write(deg_to_pulse(pos_claw));
      Serial.println(pos_claw);
    }

    Serial.print("dir_left: ");
    Serial.print(package.dir_left);
    Serial.print(" dir_right: ");
    Serial.println(package.dir_right);
    Serial.println(package.claw);
  }
}

int deg_to_pulse(int angle){
  return map(angle, 0, 180, 500, 2500);
}


void servo_drive(char servo_direction)
{
  if(servo_direction == 'f') // FWD
    {
      if(pos_servo < servo_max_deg)
      {
        pos_servo += servo_increment;
      }
    }
    
    else if(servo_direction == 'b') // BWD
    {
      if(pos_servo > servo_min_deg)
      {
        pos_servo -= servo_increment;
      }
    }

  servo.write(deg_to_pulse(pos_servo));
}