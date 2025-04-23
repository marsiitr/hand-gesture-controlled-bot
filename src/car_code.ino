#include <SoftwareSerial.h>

#define PWM_L 9   
#define PWM_R 11  
#define DIR_L 8 
#define DIR_R 10  

SoftwareSerial BTSerial(2, 3); 

String a = "";
bool startStoring = false;
int speedValue = 100;

void setSpeed(int level) {
  if (level == 1) speedValue = 40;     // Slow
  else if (level == 2) speedValue = 60; // Medium
  else if (level == 3) speedValue = 80; // Fast
}

void move(int leftSpeed, int rightSpeed, int l, int r) {
  digitalWrite(DIR_L, l);
  digitalWrite(DIR_R, r);
  analogWrite(PWM_L, leftSpeed);
  analogWrite(PWM_R, rightSpeed);
  
}

void setup() {
  pinMode(PWM_L, OUTPUT);
  pinMode(PWM_R, OUTPUT);
  pinMode(DIR_L, OUTPUT);
  pinMode(DIR_R, OUTPUT);

  BTSerial.begin(9600);
  Serial.begin(9600);
}

void loop() {
  while (BTSerial.available()) {
    char c = BTSerial.read();
    if (c == '\n' || c == ' ') continue;

    if (!startStoring && c == 's') {
      startStoring = true;
      a = "s";
      continue;
    }

    if (startStoring) {
      a += c;

      if (a.length() == 4) {
        Serial.println("Received: " + a);

        int rIndex = a.indexOf('r');
        if (rIndex > 1 && rIndex < a.length() - 1) {
          int speed = a.substring(1, rIndex).toInt();
          int direction = a.substring(rIndex + 1).toInt();
          setSpeed(speed);

          // Move based on direction
          switch (direction) {
            case 1: move(speedValue/1.5, speedValue , LOW, LOW); break;  // Reverse Left
            case 3: move(speedValue, speedValue/1.5, LOW, LOW); break;  // Reverse Right
            case 9: move(speedValue, speedValue / 1.5, HIGH, HIGH); break; // Forward Right
            case 7: move(speedValue / 1.5, speedValue, HIGH, HIGH); break; // Forward Left
            case 8: move(speedValue, speedValue, HIGH, HIGH); break;    // Forward
            case 2: move(speedValue, speedValue, LOW, LOW); break;      // Reverse
            case 6: move(speedValue, speedValue, HIGH, LOW); break;             // Right
            case 4: move(speedValue, speedValue, LOW, HIGH); break;             // Left
            default: move(0, 0, LOW, LOW); break;                       // Stop
          }

          Serial.println("Speed: " + String(speed) + ", Direction: " + String(direction));
          delay(10);  
        }
        a = "";
        startStoring = false;
      }
    }
  }
}
