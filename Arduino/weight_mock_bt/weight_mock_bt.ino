/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 55731323935351E051B0
Windows: COM8
Raspian: /dev/ttyArduinoWei
MAC: 00:0E:EA:CF:47:5A
*/

#include <SoftwareSerial.h>

#define RxD 7 // Inverse Rx and Tx if BT Grove
#define TxD 6
SoftwareSerial blueToothSerial(RxD,TxD);
int i = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting Weight mock BT");
  blueToothSerial.begin(9600);
  //setupBlueToothConnection();
  delay(1000);
}

void loop() {
  int v = 2000 + i;
  Serial.println("wei:"+String(v));
  digitalWrite(LED_BUILTIN, HIGH);
  blueToothSerial.println("wei:"+String(v));
  delay(200);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1800);
  i++;
  i %= 1000;
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
  blueToothSerial.print("AT+NAMEweightbt"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234
  delay(400);
  blueToothSerial.print("AT+AUTH0");   // No Auth
  delay(400);
  blueToothSerial.flush();
}
