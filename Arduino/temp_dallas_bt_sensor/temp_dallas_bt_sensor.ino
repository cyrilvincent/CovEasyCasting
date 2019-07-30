#include <OneWire.h>
#include <DallasTemperature.h>
#include <SoftwareSerial.h>
 
#define ONE_WIRE_BUS 2
#define RxD 7
#define TxD 6

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
SoftwareSerial blueToothSerial(RxD,TxD);
 
void setup(void)
{
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(RxD, INPUT);
  pinMode(TxD, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting");
  sensors.begin();
  setupBlueToothConnection();
  delay(1000);
  Serial.flush();
  blueToothSerial.flush();
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
  blueToothSerial.begin(9600);  
  blueToothSerial.print("AT");
  delay(400); 
  blueToothSerial.print("AT+DEFAULT"); // Restore all setup value to factory setup
  delay(2000); 
  blueToothSerial.print("AT+NAMEcovtemp"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+ROLEM"); // set the bluetooth work in master mode
  delay(400); 
  blueToothSerial.print("AT+AUTH0"); // No security blueToothSerial.print("AT+AUTH1");          
  delay(400);
  //blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234           
  //delay(400);    
  blueToothSerial.print("AT+CLEAR"); // Clear connected device mac address
  delay(400);   
  blueToothSerial.flush();
}
