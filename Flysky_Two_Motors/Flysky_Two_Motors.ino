// ===== RC PINS =====
#define CH_THROTTLE 2   // CH3 → D2
#define CH_STEERING 3   // CH1 → D3

// ===== MOTOR DRIVER PINS =====
// LEFT
#define IN1_LEFT 4
#define IN2_LEFT 6
#define IN3_LEFT 7
#define IN4_LEFT 8

// RIGHT
#define IN1_RIGHT 9
#define IN2_RIGHT 10
#define IN3_RIGHT 12
#define IN4_RIGHT A0   // instead of 13

// ENABLE (PWM)
#define ENA 5    // LEFT motors
#define ENB 11   // RIGHT motors

// ===== RC CALIBRATION =====
#define THR_CENTER 1476
#define STR_CENTER 1441

#define THR_DEAD 50
#define STR_DEAD 100

long throttle = THR_CENTER;
long steering = STR_CENTER;

// ================= SAFE CHANNEL READ =================
long readChannel(uint8_t pin, long lastValue) {
  long v = pulseIn(pin, HIGH, 25000);
  if (v < 900 || v > 2100) return lastValue;
  return v;
}

void setup() {
  Serial.begin(9600);

  pinMode(CH_THROTTLE, INPUT);
  pinMode(CH_STEERING, INPUT);

  pinMode(IN1_LEFT, OUTPUT);
  pinMode(IN2_LEFT, OUTPUT);
  pinMode(IN3_LEFT, OUTPUT);
  pinMode(IN4_LEFT, OUTPUT);

  pinMode(IN1_RIGHT, OUTPUT);
  pinMode(IN2_RIGHT, OUTPUT);
  pinMode(IN3_RIGHT, OUTPUT);
  pinMode(IN4_RIGHT, OUTPUT);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  stopMotors();

  Serial.println("=== RC CAR READY ===");
}

void loop() {

  throttle = readChannel(CH_THROTTLE, throttle);
  steering = readChannel(CH_STEERING, steering);

  Serial.print("THR: ");
  Serial.print(throttle);
  Serial.print("  STR: ");
  Serial.println(steering);

  bool thrNeutral = abs(throttle - THR_CENTER) < THR_DEAD;
  bool strLeft  = steering < (STR_CENTER - STR_DEAD);
  bool strRight = steering > (STR_CENTER + STR_DEAD);

  // ================= PIVOT TURN (NO THROTTLE) =================
  if (thrNeutral) {
    if (strLeft) {
      motorLeftReverse();
      motorRightForward();
    }
    else if (strRight) {
      motorLeftForward();
      motorRightReverse();
    }
    else {
      stopMotors();
    }
    return;
  }

  bool forward = throttle > THR_CENTER;

  // ================= MOVE + STEER =================
  if (forward) {
    if (strLeft) {
      motorLeftStop();
      motorRightForward();
    }
    else if (strRight) {
      motorLeftForward();
      motorRightStop();
    }
    else {
      motorLeftForward();
      motorRightForward();
    }
  }
  else { // REVERSE
    if (strLeft) {
      motorLeftStop();
      motorRightReverse();
    }
    else if (strRight) {
      motorLeftReverse();
      motorRightStop();
    }
    else {
      motorLeftReverse();
      motorRightReverse();
    }
  }
}

// ================= MOTOR FUNCTIONS =================
void motorLeftForward() {
  analogWrite(ENA, 225);
  digitalWrite(IN1_LEFT, HIGH);
  digitalWrite(IN2_LEFT, LOW);
  digitalWrite(IN3_LEFT, LOW);
  digitalWrite(IN4_LEFT, HIGH);
}

void motorLeftReverse() {
  analogWrite(ENA, 225);
  digitalWrite(IN1_LEFT, LOW);
  digitalWrite(IN2_LEFT, HIGH);
  digitalWrite(IN3_LEFT, HIGH);
  digitalWrite(IN4_LEFT, LOW);
}

void motorRightForward() {
  analogWrite(ENB, 225);
  digitalWrite(IN1_RIGHT, HIGH);
  digitalWrite(IN2_RIGHT, LOW);
  digitalWrite(IN3_RIGHT, LOW);
  digitalWrite(IN4_RIGHT, HIGH);
}

void motorRightReverse() {
  analogWrite(ENB, 225);
  digitalWrite(IN1_RIGHT, LOW);
  digitalWrite(IN2_RIGHT, HIGH);
  digitalWrite(IN3_RIGHT, HIGH);
  digitalWrite(IN4_RIGHT, LOW);
}

// ===== PER-SIDE STOP (THIS WAS MISSING) =====
void motorLeftStop() {
  analogWrite(ENA, 0);
  digitalWrite(IN1_LEFT, LOW);
  digitalWrite(IN2_LEFT, LOW);
  digitalWrite(IN3_LEFT, LOW);
  digitalWrite(IN4_LEFT, LOW);
}

void motorRightStop() {
  analogWrite(ENB, 0);
  digitalWrite(IN1_RIGHT, LOW);
  digitalWrite(IN2_RIGHT, LOW);
  digitalWrite(IN3_RIGHT, LOW);
  digitalWrite(IN4_RIGHT, LOW);
}

// ===== FULL STOP =====
void stopMotors() {
  motorLeftStop();
  motorRightStop();
}

