// ============================================================
//   RHINO MDD20AMP + ARDUINO NANO + FS-i6X (FINAL VERSION)
// ============================================================

#define CH1_PIN 2
#define CH2_PIN 3

volatile unsigned long ch1_start = 0, ch2_start = 0;
volatile int ch1_val = 0, ch2_val = 0;

// Motor Driver Pins
const int PWM1 = 5;  // Left Speed
const int DIR1 = 4;  // Left Direction

const int PWM2 = 6;  // Right Speed
const int DIR2 = 7;  // Right Direction

const int RES_MIN = 1000;
const int RES_MAX = 2000;

// 🔧 OFFSET VALUES (based on your readings)
int ch1_offset = 18;
int ch2_offset = -19;

// ============================================================
// INTERRUPTS
// ============================================================

void ch1_ISR() {
  if (digitalRead(CH1_PIN)) ch1_start = micros();
  else {
    unsigned long w = micros() - ch1_start;
    if (w >= 900 && w <= 2100)
      ch1_val = map(w, RES_MIN, RES_MAX, -255, 255);
  }
}

void ch2_ISR() {
  if (digitalRead(CH2_PIN)) ch2_start = micros();
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

  pinMode(PWM1, OUTPUT);
  pinMode(DIR1, OUTPUT);
  pinMode(PWM2, OUTPUT);
  pinMode(DIR2, OUTPUT);

  stopMotors();

  Serial.println("✅ Rhino Driver Ready (Calibrated)");
}

// ============================================================

void loop() {

  int throttle = ch2_val - ch2_offset;
  int steering = ch1_val - ch1_offset;

  if (abs(throttle) < 30) throttle = 0;
  if (abs(steering) < 30) steering = 0;

  int leftSpeed, rightSpeed;

  // ✅ FIX: Straight motion correction
  if (abs(steering) < 40) {
    leftSpeed  = throttle;
    rightSpeed = throttle;
  } else {
    leftSpeed  = throttle + steering;
    rightSpeed = throttle - steering;
  }

  if (abs(leftSpeed) < 50) leftSpeed = 0;
  if (abs(rightSpeed) < 50) rightSpeed = 0;

  leftSpeed  = constrain(leftSpeed, -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  Serial.print("CH1: "); Serial.print(ch1_val);
  Serial.print(" | CH2: "); Serial.print(ch2_val);
  Serial.print(" | L: "); Serial.print(leftSpeed);
  Serial.print(" | R: "); Serial.println(rightSpeed);

  driveMotor(PWM1, DIR1, leftSpeed);
  driveMotor(PWM2, DIR2, rightSpeed);

  delay(20);
}

// ============================================================
// MOTOR CONTROL FUNCTION
// ============================================================

void driveMotor(int pwmPin, int dirPin, int speed) {

  if (speed > 0) {
    digitalWrite(dirPin, HIGH);
    analogWrite(pwmPin, speed);
  }
  else if (speed < 0) {
    digitalWrite(dirPin, LOW);
    analogWrite(pwmPin, -speed);
  }
  else {
    analogWrite(pwmPin, 0);
  }
}

// ============================================================

void stopMotors() {
  analogWrite(PWM1, 0);
  analogWrite(PWM2, 0);
}