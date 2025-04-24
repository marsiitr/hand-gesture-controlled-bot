#include <SoftwareSerial.h>

SoftwareSerial BTSerial(2, 3); // RX, TX

String inputString = "";

void setup() {
  Serial.begin(9600);    // Serial Monitor
  BTSerial.begin(9600);  // Bluetooth Module Baud Rate
}

void loop() {
  while (Serial.available()) {
    char receivedChar = Serial.read();
    
    inputString += receivedChar;

    if (receivedChar == '\n') {
      BTSerial.print(inputString);  // Send to Bluetooth
      inputString = "";             // Clear the string for next input
    }
  }
}
