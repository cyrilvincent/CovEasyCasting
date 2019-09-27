/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 85730313936351410222
Windows: COM12
Raspian: /dev/ttyArduinoMix
 */

#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);
  lcd.print("Starting Mix");
  Serial.begin(9600);
  Serial.println("Starting Mix");
  Serial.println("mix:0");
  delay(1000);
  lcd.setRGB(255, 0, 0);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("->");
  lcd.setCursor(0,1);
  lcd.print("<-100000");
}

void loop() {
  if(Serial.available() > 0) {
    lcd.setRGB(0,255,0);
    delay(100);
    int data = Serial.readStringUntil('\n').toInt();
    digitalWrite(LED_BUILTIN, HIGH);
    char s[8];
    itoa(data + 32,s,2);
    lcd.setCursor(2,0);
    lcd.print(String(data)+" ");
    lcd.setCursor(2,1);
    lcd.print(String(s)+" ");
    Serial.println("mix:"+String(s));
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    lcd.setRGB(255, 255, 255);
    
  }
}
