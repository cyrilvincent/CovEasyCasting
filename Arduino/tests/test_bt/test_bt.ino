#include <SoftwareSerial.h>
 
#define RxD 7 // Rx = 7 Tx = 6 for shield (on board Rx = 6 Tx = 7) Rx = 6 Tx = 7 for grove
#define TxD 6

#define DEBUG_ENABLED  1

SoftwareSerial blueToothSerial(RxD,TxD);
int i = 0;

void setup(void)
{
  Serial.begin(9600);
  Serial.println("Starting");
  //pinMode(RxD, INPUT);
  //pinMode(TxD, OUTPUT);
  blueToothSerial.begin(9600);
  //setupBlueToothConnection();

  delay(1000);
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
  //blueToothSerial.print("AT+DEFAULT");             // Restore all setup value to factory setup
  //delay(2000); 
  blueToothSerial.print("AT+NAMESeeedBTSlave");    // set the bluetooth name as "SeeedBTSlave" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN0000");             // set the pair code to connect 
  delay(400);
  blueToothSerial.print("AT+AUTH0");             //
  delay(400);    
  blueToothSerial.flush();
  Serial.println("End Setup BT");
}
