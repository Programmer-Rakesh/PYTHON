// ── Motor pins ────────────────────────────────────────────────────────────
#define ENA 5
#define IN1 6
#define IN2 7
#define IN3 8
#define IN4 9
#define ENB 10

// ── IR sensors ────────────────────────────────────────────────────────────
#define IR_LEFT   22
#define IR_MID    24
#define IR_RIGHT  26

// ── Ultrasonic sensor (front only) ───────────────────────────────────────
#define TRIG_FRONT 30
#define ECHO_FRONT 31

#define BUZZER    11

// ── Detection range: increase if crashing, decrease if stopping too early ─
#define MAX_RANGE 45        // ← CALIBRATE: raise this (e.g. 50-60) if still crashing

// ── Speed settings ────────────────────────────────────────────────────────
#define SPEED_BASE    130   // ← CALIBRATE: lower if still too fast (try 110-150)
#define COMPENSATION   25   // ← CALIBRATE: adjust if robot drifts left/right
#define SPEED_RIGHT   SPEED_BASE
#define SPEED_LEFT    (SPEED_BASE + COMPENSATION)

#define TURN_SPEED    160   // ← CALIBRATE: lower = slower turns, easier to tune angle
#define TURN_RIGHT_MS 520   // ← CALIBRATE: increase if turning less than 90°, decrease if more
#define TURN_LEFT_MS  540   // ← CALIBRATE: tune independently if left/right turns differ

// =========================================================================
//  Ultrasonic helper
// =========================================================================
int readPing(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH, 30000);
  int cm = duration * 0.034 / 2;
  if (cm == 0) cm = 200;
  return cm;
}

// =========================================================================
//  Motor helpers
// =========================================================================
void stopMotors() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void moveForward() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);   // RIGHT motor FORWARD
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);   // LEFT  motor FORWARD
  analogWrite(ENA, SPEED_RIGHT);
  analogWrite(ENB, SPEED_LEFT);
}

void moveBackward() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);  // RIGHT motor BACKWARD
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);  // LEFT  motor BACKWARD
  analogWrite(ENA, SPEED_RIGHT);
  analogWrite(ENB, SPEED_LEFT);
}

// ── TANK TURN RIGHT: Left FORWARD, Right BACKWARD ────────────────────────
void turnRight() {
  digitalWrite(IN1, LOW);  digitalWrite(IN2, HIGH);  // RIGHT → BACKWARD
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);   // LEFT  → FORWARD
  analogWrite(ENA, TURN_SPEED);
  analogWrite(ENB, TURN_SPEED);
  delay(TURN_RIGHT_MS);   // ← CALIBRATE via TURN_RIGHT_MS above
  stopMotors();
  delay(200);
}

// ── TANK TURN LEFT: Right FORWARD, Left BACKWARD ─────────────────────────
void turnLeft() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);   // RIGHT → FORWARD
  digitalWrite(IN3, LOW);  digitalWrite(IN4, HIGH);  // LEFT  → BACKWARD
  analogWrite(ENA, TURN_SPEED);
  analogWrite(ENB, TURN_SPEED);
  delay(TURN_LEFT_MS);    // ← CALIBRATE via TURN_LEFT_MS above
  stopMotors();
  delay(200);
}

// =========================================================================
//  Setup
// =========================================================================
void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT); pinMode(ENB, OUTPUT);

  pinMode(IR_LEFT,  INPUT);
  pinMode(IR_MID,   INPUT);
  pinMode(IR_RIGHT, INPUT);

  pinMode(TRIG_FRONT, OUTPUT); pinMode(ECHO_FRONT, INPUT);

  pinMode(BUZZER, OUTPUT);

  moveForward();
}

// =========================================================================
//  Loop
// =========================================================================
void loop() {

  int irL = digitalRead(IR_LEFT);
  int irM = digitalRead(IR_MID);
  int irR = digitalRead(IR_RIGHT);

  int distFront = readPing(TRIG_FRONT, ECHO_FRONT);

  Serial.print("IR L:"); Serial.print(irL);
  Serial.print(" M:");   Serial.print(irM);
  Serial.print(" R:");   Serial.print(irR);
  Serial.print(" | FRONT: "); Serial.println(distFront);

  // ── PRIORITY 1: Ultrasonic ────────────────────────────────────────────
  if (distFront <= MAX_RANGE) {

    // 1. Stop + beep
    stopMotors();
    digitalWrite(BUZZER, HIGH);
    delay(300);
    digitalWrite(BUZZER, LOW);
    Serial.println(">> OBSTACLE - starting avoidance");

    // 2. Go backward
    Serial.println(">> Backing up");
    moveBackward();
    delay(400);             // ← CALIBRATE: increase if not backing up enough
    stopMotors();
    delay(200);

    // 3. Tank turn RIGHT ~90°
    Serial.println(">> Turning RIGHT");
    turnRight();
    delay(200);

    // 4. Move forward to clear obstacle
    Serial.println(">> Moving forward");
    moveForward();
    delay(800);             // ← CALIBRATE: increase if obstacle not fully cleared
    stopMotors();
    delay(200);

    // 5. Tank turn LEFT ~90° to straighten
    Serial.println(">> Turning LEFT");
    turnLeft();
    delay(200);

    // 6. Move forward a little then stop permanently
    Serial.println(">> Final move");
    moveForward();
    delay(1200);             // ← CALIBRATE: how far it moves after final left turn
    stopMotors();

    Serial.println(">> DONE - press reset to run again");
    while(true);            // ← halts forever, press reset button to restart
  }

  digitalWrite(BUZZER, LOW);

  // ── PRIORITY 2: IR boundary ───────────────────────────────────────────
  // WHITE = LOW = stop    BLACK = HIGH = move
  bool irStop = (irL == LOW && irM == LOW) ||
                (irR == LOW && irM == LOW) ||
                (irL == LOW && irM == LOW && irR == LOW);

  if (irStop) {
    stopMotors();
  } else {
    moveForward();
  }

  delay(50);
}