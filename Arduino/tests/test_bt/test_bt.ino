#include <SoftwareSerial.h>
 
#define RxD 6
#define TxD 7

SoftwareSerial blueToothSerial(RxD,TxD);
int i = 0;

void setup(void)
{
  Serial.begin(9600);
  Serial.println("Starting");
  setupBlueToothConnection();
  delay(1000);
  blueToothSerial.println(i);
  blueToothSerial.flush();
}
 
 
void loop(void)
{
  Serial.println(i);
  blueToothSerial.println(i);
  digitalWrite(LED_BUILTIN, HIGH);
  i++;
  delay(1000);
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
  blueToothSerial.print("AT+NAMEtestbt"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234
  delay(400);
  blueToothSerial.print("AT+AUTH0");   // No Auth
  delay(400);
  blueToothSerial.flush();
}
