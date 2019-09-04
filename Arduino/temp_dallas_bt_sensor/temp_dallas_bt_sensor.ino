#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>
 
#define ONE_WIRE_BUS 2
#define RxD 6
#define TxD 7

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
SoftwareSerial blueToothSerial(RxD,TxD);
 
void setup(void)
{
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting Dallas temp sensor + BT");
  blueToothSerial.begin(9600);
  sensors.begin();
  setupBlueToothConnection();
  delay(1000);
}
 
 
void loop(void)
{
  sensors.requestTemperatures();
  float temp = sensors.getTempCByIndex(0);
  Serial.println(temp);
  blueToothSerial.println(temp);
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
  blueToothSerial.print("AT+NAMEtempbt"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234
  delay(400);
  blueToothSerial.print("AT+AUTH0");   // No Auth
  delay(400);
  blueToothSerial.flush();
}