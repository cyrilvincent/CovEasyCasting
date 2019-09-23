#include <SoftwareSerial.h>

#define RxD 6
#define TxD 7

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
  if (Serial.available() > 0) {
    Serial.println("wei:"+String(2000 + i++ % 1000));
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1800);
  }
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
