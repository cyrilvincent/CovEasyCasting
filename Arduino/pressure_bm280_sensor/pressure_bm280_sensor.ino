/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 857303139363515181D2
Windows: COM8
Raspian: /dev/ttyArduinoPre
 */

#include "Seeed_BME280.h"

// Plug on port I2C
// http://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/
// Unit: Pa
BME280 bme280;
 
void setup(void)
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting preasure BM280");
  delay(1000);
  int i = bme280.init();
  Serial.println("pre:"+String(i)); 
}

void loop(void)
{
    float pre = bme280.getPressure();
    Serial.println("pre:"+String(pre));
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(4800);
}
