int i = 0;

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Begin");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println(i++);
  delay(1000);                       
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println(i++);
  delay(1000);                   
}
