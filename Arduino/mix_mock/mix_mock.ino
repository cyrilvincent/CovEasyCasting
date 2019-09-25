/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 85730313936351410222
Windows: COM12
Raspian:
 */

#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin(16, 2);
  lcd.print("0");
  Serial.begin(9600);
  Serial.println("Starting Mix");
  Serial.println("mix:0");
}

void loop() {
  if(Serial.available() > 0) {
    int data = Serial.readStringUntil('\n').toInt();
    digitalWrite(LED_BUILTIN, HIGH);
    //Serial.println("mix:"+String(data));
    char s[8];
    itoa(data + 32,s,2);
    lcd.clear()
    lcd.write(String(s))
    Serial.println("mix:"+String(s));
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
  }
}
