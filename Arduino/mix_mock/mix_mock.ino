int data = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  while (Serial.available() > 0) {
    data = Serial.readStringUntil('\n').toInt();
    //int in_data = Serial.parseInt();
    digitalWrite(LED_BUILTIN, HIGH);
    delay(200);
    Serial.println("1");
    digitalWrite(LED_BUILTIN, LOW); 
  }
}
