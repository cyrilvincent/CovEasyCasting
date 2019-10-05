/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 85730313936351410222
Windows: COM12
Raspian: /dev/ttyArduinoMix
RS232VID: 0x067b
RS232PID: 0x2303
RS232dev: /dev/ttyArduinoRS
*/

#include <Wire.h>
#include "rgb_lcd.h"
#include <SoftwareSerial.h>

SoftwareSerial mySerial(7, 6);

rgb_lcd lcd;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);
  lcd.print("Starting Mix");
  Serial.begin(9600);
  mySerial.begin(9600);
  Serial.println("Starting Mix");
  Serial.println("mix:100000");
  mySerial.println("mix:100000");
  delay(1000);
  lcd.setRGB(255, 0, 0);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("->");
  lcd.setCursor(0,1);
  lcd.print("<-100000");
}

void loop() {
  //if(Serial.available() > 0) {
  if(mySerial.available() > 0) {
    lcd.setRGB(0,255,0);
    delay(100);
    //int data = Serial.readStringUntil('\n').toInt();
    int data = mySerial.readStringUntil('\n').toInt();
    digitalWrite(LED_BUILTIN, HIGH);
    char s[8];
    itoa(data + 32,s,2);
    lcd.setCursor(2,0);
    lcd.print(String(data)+" ");
    lcd.setCursor(2,1);
    lcd.print(String(s)+" ");
    Serial.println("mix:"+String(s));
    mySerial.println("mix:"+String(s));
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    lcd.setRGB(255, 255, 255);
    
  }
}
