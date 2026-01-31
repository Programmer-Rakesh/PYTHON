#include <Wire.h>
#include <MPU6050.h>
#include <Servo.h>

#define PPM_PIN 2
#define CHANNELS 6

#define M1_PIN 3
#define M2_PIN 5
#define M3_PIN 6
#define M4_PIN 9

#define MIN_THROTTLE 1000
#define IDLE_THROTTLE 1020
#define MAX_THROTTLE 1800
#define PID_THROTTLE_CUTOFF 1080


MPU6050 mpu;
Servo m1, m2, m3, m4;

// ---------- PPM ----------
volatile uint16_t ppm[CHANNELS];
volatile uint8_t ch = 0;
volatile uint32_t lastTime = 0;

bool ppmValid = false;
unsigned long lastPPMTime = 0;

void ppmISR() {
  uint32_t now = micros();
  uint32_t diff = now - lastTime;
  lastTime = now;

  if (diff > 3000) {
    ch = 0;
    ppmValid = true;
    lastPPMTime = millis();
  } else if (ch < CHANNELS) {
    ppm[ch++] = diff;
  }
}

// ---------- PID ----------
float kp = 2.0;
float ki = 0.01;
float kd = 1.2;

float rollPID = 0, pitchPID = 0;
float rollError = 0, pitchError = 0;
float rollI = 0, pitchI = 0;
float lastRollError = 0, lastPitchError = 0;

// ---------- State ----------
bool armed = false;
unsigned long armTimer = 0;

// ---------- Helpers ----------
void writeMotors(int val) {
  m1.writeMicroseconds(val);
  m2.writeMicroseconds(val);
  m3.writeMicroseconds(val);
  m4.writeMicroseconds(val);
}

// ---------- Setup ----------
void setup() {
  Serial.begin(115200);

  pinMode(PPM_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PPM_PIN), ppmISR, RISING);

  for (int i = 0; i < CHANNELS; i++) ppm[i] = 1500;
  ppm[2] = 1000;
  ppm[3] = 1500;

  Wire.begin();
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU FAIL");
    while (1);
  }

  m1.attach(M1_PIN);
  m2.attach(M2_PIN);
  m3.attach(M3_PIN);
  m4.attach(M4_PIN);

  writeMotors(MIN_THROTTLE);
  Serial.println("FC READY - DISARMED");
}

// ---------- Loop ----------
void loop() {

  // FAILSAFE
  if (!ppmValid || millis() - lastPPMTime > 500) {
    armed = false;
    writeMotors(MIN_THROTTLE);
    rollI = pitchI = 0;
    return;
  }

  int rollIn     = ppm[0];
  int pitchIn    = ppm[1];
  int throttleIn = ppm[2];
  int yawIn      = ppm[3];

  // ARM / DISARM
  if (throttleIn < 1050 && yawIn > 1900) {
    if (!armed && millis() - armTimer > 800) {
      armed = true;
      rollI = pitchI = 0;
      lastRollError = lastPitchError = 0;
    }
  }
  else if (throttleIn < 1050 && yawIn < 1100) {
    armed = false;
    armTimer = millis();
    rollI = pitchI = 0;
  }
  else {
    armTimer = millis();
  }

  // READ MPU
  int16_t ax, ay, az, gx, gy, gz;
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

  float rollAngle  = atan2(ay, az) * 57.3;
  float pitchAngle = atan2(-ax, az) * 57.3;

  float rollTarget  = map(rollIn, 1000, 2000, -20, 20);
  float pitchTarget = map(pitchIn, 1000, 2000, -20, 20);

  // PID
  // rollError  = rollTarget  - rollAngle;
  // pitchError = pitchTarget - pitchAngle;

  // rollI  += rollError;
  // pitchI += pitchError;

  // rollI  = constrain(rollI,  -300, 300);
  // pitchI = constrain(pitchI, -300, 300);

  // rollPID  = kp * rollError  + ki * rollI  + kd * (rollError  - lastRollError);
  // pitchPID = kp * pitchError + ki * pitchI + kd * (pitchError - lastPitchError);

  // rollPID  = constrain(rollPID,  -200, 200);
  // pitchPID = constrain(pitchPID, -200, 200);

  // lastRollError  = rollError;
  // lastPitchError = pitchError;

rollError  = rollTarget  - rollAngle;
pitchError = pitchTarget - pitchAngle;

if (throttleIn > PID_THROTTLE_CUTOFF) {

  rollI  += rollError;
  pitchI += pitchError;

  rollI  = constrain(rollI,  -300, 300);
  pitchI = constrain(pitchI, -300, 300);

  rollPID  = kp * rollError  + ki * rollI  + kd * (rollError  - lastRollError);
  pitchPID = kp * pitchError + ki * pitchI + kd * (pitchError - lastPitchError);

} else {
  // Throttle low → no stabilization force
  rollI = pitchI = 0;
  rollPID = pitchPID = 0;
}

rollPID  = constrain(rollPID,  -200, 200);
pitchPID = constrain(pitchPID, -200, 200);

lastRollError  = rollError;
lastPitchError = pitchError;


  // MOTOR MIX
  if (!armed) {
    writeMotors(MIN_THROTTLE);
  } else {

    int base = (throttleIn < 1050) ? IDLE_THROTTLE :
               constrain(throttleIn, IDLE_THROTTLE, MAX_THROTTLE);

    m1.writeMicroseconds(constrain(base - rollPID + pitchPID, IDLE_THROTTLE, 2000));
    m2.writeMicroseconds(constrain(base - rollPID - pitchPID, IDLE_THROTTLE, 2000));
    m3.writeMicroseconds(constrain(base + rollPID - pitchPID, IDLE_THROTTLE, 2000));
    m4.writeMicroseconds(constrain(base + rollPID + pitchPID, IDLE_THROTTLE, 2000));
  }
}
