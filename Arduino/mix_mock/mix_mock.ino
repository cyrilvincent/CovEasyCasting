int data = 0;
int res = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Starting Mix");
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  while (Serial.available() > 0) {
    data = Serial.readStringUntil('\n').toInt();
    //int data = Serial.parseInt();
    digitalWrite(LED_BUILTIN, HIGH);
    if((data > 0) && (data <= 5)) {
        res = 1;
    }
    Serial.println(res);
    delay(200);
    digitalWrite(LED_BUILTIN, LOW); 
  }
}
