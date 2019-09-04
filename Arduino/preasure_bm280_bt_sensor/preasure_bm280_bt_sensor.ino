#include "Seeed_BME280.h"
#include <Wire.h>
#include <SoftwareSerial.h>
 
#define RxD 6
#define TxD 7
// Plug on port I2C
// http://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/

BME280 bme280;
SoftwareSerial blueToothSerial(RxD,TxD);
 
void setup(void)
{
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting preasure BM280 + BT");
  blueToothSerial.begin(9600);
  setupBlueToothConnection();
  delay(1000);
  if(!bme280.init()){
    Serial.println("Device error!");
    blueToothSerial.println(-1);
  }
}
 
 
void loop(void)
{
  float preasure = bme280.getPressure();
  Serial.println(preasure);
  blueToothSerial.println(preasure);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(200);
  digitalWrite(LED_BUILTIN, LOW);
  delay(800);
}

void setupBlueToothConnection()
{
  // http://wiki.seeedstudio.com/Grove-Serial_Bluetooth_v3.0/
  // See also https://www.teachmemicro.com/arduino-bluetooth/
  Serial.println("Setup BT");
  blueToothSerial.print("AT");
  delay(400);
  blueToothSerial.print("AT+DEFAULT"); // Restore all setup value to factory setup
  delay(2000);
  blueToothSerial.print("AT+NAMEpreasbt"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234
  delay(400);
  blueToothSerial.print("AT+AUTH0");   // No Auth
  delay(400);
  blueToothSerial.flush();
}
