// 5 أزرار — كل ضغطة ترسل رقم الزر (1-5) للكمبيوتر
// التوصيل: Pin -> طرف الزر | GND -> الطرف الآخر (INPUT_PULLUP)
//
// Pin 4  -> 1  (mardid)
// Pin 8  -> 2  (jordan)
// Pin 9  -> 3  (wehdat)
// Pin 10 -> 4  (faisaly)
// Pin 11 -> 5  (baracalona)

const int NUM_BUTTONS = 5;
const int BUTTON_PINS[] = {4, 8, 9, 10, 11};
const unsigned long DEBOUNCE_MS = 60;

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
