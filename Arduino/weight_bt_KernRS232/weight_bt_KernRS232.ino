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

#define RxD_RS 4 // Port RS232 balance
#define TxD_RS 5
SoftwareSerial RS232_Serial(RxD_RS,TxD_RS);

int timeout=0 ;
 
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting Weight BT");
  blueToothSerial.begin(9600);
  RS232_Serial.begin(9600);
//setupBlueToothConnection();
  delay(1000);
}

void loop() {

  timeout++;
  
  if(RS232_Serial.available() > 0) {
     timeout = 0;   
     float val = 9999; // Si defaut ou negatif
     
     String s = RS232_Serial.readStringUntil('\n');
     s.trim(); //Supprime les espaces
     int pos = s.indexOf("g"); // Renvoi position du g -1 si pas trouve
     if (pos >-1 && s.indexOf("-")== -1){ // Si pas de g et pas de - valeur 
        s = s.substring(0,pos-1);   
        val = s.toFloat();
     }   
     Serial.println(val);
     blueToothSerial.println("wei:"+String(val));  
  }
  delay(100);
  if (timeout > 50) {
    Serial.println(8888);
     blueToothSerial.println("wei:"+String(8888));
   delay(1000);
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
