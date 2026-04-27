#include <Servo.h>

Servo servoHand;
const int servoPin = 9;
bool sequenceDone = false;

void setup() {
  servoHand.attach(servoPin);
  servoHand.write(0);
}

void loop() {
  if (sequenceDone) {
    return;
  }

  delay(1000);
  servoHand.write(90);
  delay(2000);
  servoHand.write(0);
  servoHand.detach();
  sequenceDone = true;
}
