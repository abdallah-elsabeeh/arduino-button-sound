// 5 أزرار — Pins 2,3,4,5,6 — كل ضغطة ترسل رقم الزر (1-5)

const int NUM_BUTTONS = 5;
const int BUTTON_PINS[] = {2, 3, 4, 5, 6};
const unsigned long DEBOUNCE_MS = 50;

bool lastReading[NUM_BUTTONS];
bool stableState[NUM_BUTTONS];
unsigned long lastDebounce[NUM_BUTTONS];

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < NUM_BUTTONS; i++) {
    pinMode(BUTTON_PINS[i], INPUT_PULLUP);
    lastReading[i] = HIGH;
    stableState[i] = HIGH;
    lastDebounce[i] = 0;
  }
}

void loop() {
  for (int i = 0; i < NUM_BUTTONS; i++) {
    int reading = digitalRead(BUTTON_PINS[i]);

    if (reading != lastReading[i]) {
      lastDebounce[i] = millis();
    }

    if ((millis() - lastDebounce[i]) > DEBOUNCE_MS) {
      if (reading == LOW && stableState[i] == HIGH) {
        Serial.println(i + 1);
      }
      stableState[i] = reading;
    }

    lastReading[i] = reading;
  }
}
