/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 857303139363515181D2
Windows: COM8
Raspian: /dev/ttyArduinoPre
 */
/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 75735353238351205232
*/
#include "Seeed_BME280.h"
#include <SoftwareSerial.h>

// Plug on port I2C
// http://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/
// Unit: Pa
BME280 bme280;

#define RxD 6
#define TxD 7

SoftwareSerial blueToothSerial(RxD,TxD);

void setup(void)
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting preasure BM280");
  
  int i = bme280.init();
  Serial.println("pre:"+String(i)); 
  blueToothSerial.begin(9600);
//  setupBlueToothConnection();
  delay(1000);
 
}

void loop(void)
{
    float pre = bme280.getPressure();
    Serial.println("pre:"+String(pre));
    blueToothSerial.println("pre:"+String(pre));
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1800);
    
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
  blueToothSerial.print("AT+NAMEprebt"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234           
  delay(400);    
  blueToothSerial.print("AT+AUTH0");   // No Auth     
  delay(400);
  blueToothSerial.flush();
}
