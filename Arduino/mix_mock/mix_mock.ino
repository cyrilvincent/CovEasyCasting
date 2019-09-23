int data = 0;
int res = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting Mix");
  //while (!Serial) {
  //  ; // wait for serial port to connect. Needed for native USB port only
  //}
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.readStringUntil('\n').toInt();
    //int data = Serial.parseInt();
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("mix"+String(data));
    delay(200);
    digitalWrite(LED_BUILTIN, LOW); 
  }
}
