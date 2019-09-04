#include <SoftwareSerial.h>
#include <math.h>

#define ONE_WIRE_BUS 2
#define RxD 6
#define TxD 7

const int B = 4275;               // B value of the thermistor
const int R0 = 100000;            // R0 = 100k
const int pinTempSensor = A0;     // Grove - Temperature Sensor connect to A0

SoftwareSerial blueToothSerial(RxD,TxD);
 
void setup(void)
{
  Serial.begin(9600);
  Serial.println("Starting temp sensor 1.2 + BT");
  blueToothSerial.begin(9600);
  //setupBlueToothConnection();
  delay(1000);
}
 
 
void loop(void)
{
  int a = analogRead(pinTempSensor);
  float R = 1023.0/a-1.0;
  R = R0*R;
  float temp = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet
  Serial.println(temp);
  blueToothSerial.println(temp);
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
  blueToothSerial.print("AT+NAMEtempbt"); // set the bluetooth name as "SeeedMaster" ,the length of bluetooth name must less than 12 characters.
  delay(400);
  blueToothSerial.print("AT+PIN1234"); // PIN Code default 1234           
  delay(400);    
  blueToothSerial.print("AT+AUTH0");   // No Auth     
  delay(400);
  blueToothSerial.flush();
}
