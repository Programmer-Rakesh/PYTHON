// ============================================================
//   RC CAR - All 4 EN pins on PWM
// ============================================================

#define CH1_PIN 2
#define CH2_PIN 3

volatile unsigned long ch1_start = 0, ch2_start = 0;
volatile int ch1_val = 0, ch2_val = 0;

// === L298N #1 LEFT ===
const int ENA_L = 5;   // PWM ✅
const int IN1_L = 4;
const int IN2_L = 7;
const int ENB_L = 6;   // PWM ✅
const int IN3_L = 8;
const int IN4_L = 11;

// === L298N #2 RIGHT ===
const int ENA_R = 9;   // PWM ✅
const int IN1_R = 12;
const int IN2_R = 13;
const int ENB_R = 10;  // PWM ✅
const int IN3_R = A0;
const int IN4_R = A1;

const int RES_MIN = 1000;
const int RES_MAX = 2000;

// ============================================================
void ch1_ISR() {
  if (digitalRead(CH1_PIN) == HIGH) ch1_start = micros();
  else {
    unsigned long w = micros() - ch1_start;
    if (w >= 900 && w <= 2100)
      ch1_val = map(w, RES_MIN, RES_MAX, -255, 255);
  }
}

void ch2_ISR() {
  if (digitalRead(CH2_PIN) == HIGH) ch2_start = micros();
  else {
    unsigned long w = micros() - ch2_start;
    if (w >= 900 && w <= 2100)
      ch2_val = map(w, RES_MIN, RES_MAX, -255, 255);
  }
}

// ============================================================
void setup() {
  Serial.begin(9600);

  pinMode(CH1_PIN, INPUT);
  pinMode(CH2_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(CH1_PIN), ch1_ISR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(CH2_PIN), ch2_ISR, CHANGE);

  pinMode(ENA_L, OUTPUT); pinMode(IN1_L, OUTPUT); pinMode(IN2_L, OUTPUT);
  pinMode(ENB_L, OUTPUT); pinMode(IN3_L, OUTPUT); pinMode(IN4_L, OUTPUT);
  pinMode(ENA_R, OUTPUT); pinMode(IN1_R, OUTPUT); pinMode(IN2_R, OUTPUT);
  pinMode(ENB_R, OUTPUT); pinMode(IN3_R, OUTPUT); pinMode(IN4_R, OUTPUT);

  stopAll();
  Serial.println("Ready — All 4 EN pins on PWM");
}

// ============================================================
void loop() {
  int leftSpeed  = ch1_val;   // CH1 → Left motors directly
  int rightSpeed = -ch2_val;  // CH2 → Right motors INVERTED

  Serial.print("Left: "); Serial.print(leftSpeed);
  Serial.print(" | Right: "); Serial.println(rightSpeed);

  // Deadzone
  if (abs(leftSpeed)  < 50) leftSpeed  = 0;
  if (abs(rightSpeed) < 50) rightSpeed = 0;

  leftSpeed  = constrain(leftSpeed,  -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  driveLeft(leftSpeed);
  driveRight(rightSpeed);

  delay(20);
}

// ============================================================
void driveLeft(int spd) {
  int a = LOW, b = LOW;
  if      (spd > 0) { a = HIGH; b = LOW; }
  else if (spd < 0) { a = LOW; b = HIGH; spd = -spd; }
  int s = constrain(spd, 0, 255);

  digitalWrite(IN1_L, a); digitalWrite(IN2_L, b); analogWrite(ENA_L, s);
  digitalWrite(IN3_L, a); digitalWrite(IN4_L, b); analogWrite(ENB_L, s);
}

void driveRight(int spd) {
  int a = LOW, b = LOW;
  if      (spd > 0) { a = HIGH; b = LOW; }
  else if (spd < 0) { a = LOW; b = HIGH; spd = -spd; }
  int s = constrain(spd, 0, 255);

  digitalWrite(IN1_R, a); digitalWrite(IN2_R, b); analogWrite(ENA_R, s);
  digitalWrite(IN3_R, a); digitalWrite(IN4_R, b); analogWrite(ENB_R, s);
}

void stopAll() {
  analogWrite(ENA_L, 0); digitalWrite(IN1_L, LOW); digitalWrite(IN2_L, LOW);
  analogWrite(ENB_L, 0); digitalWrite(IN3_L, LOW); digitalWrite(IN4_L, LOW);
  analogWrite(ENA_R, 0); digitalWrite(IN1_R, LOW); digitalWrite(IN2_R, LOW);
  analogWrite(ENB_R, 0); digitalWrite(IN3_R, LOW); digitalWrite(IN4_R, LOW);
}
