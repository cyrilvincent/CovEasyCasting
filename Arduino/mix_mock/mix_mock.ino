/*
BN: Arduino/Genuino Uno
VID: 0x2341
PID: 0x0043
SN: 85730313936351410222
Windows: COM12
Raspian:
 */

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting Mix");
  Serial.println("mix:0");
}

void loop() {
  if(Serial.available() > 0) {
    int data = Serial.readStringUntil('\n').toInt();
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("mix:"+String(data));
    delay(200);
    digitalWrite(LED_BUILTIN, LOW);
  }
}
