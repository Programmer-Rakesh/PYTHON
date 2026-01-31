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
float kp = 1.2;
float ki = 0.015;
float kd = 0.7;

float rollPID = 0, pitchPID = 0;
float rollError = 0, pitchError = 0;
float rollI = 0, pitchI = 0;
float lastRollError = 0, lastPitchError = 0;

float yawRate;
float yawError;
float yawPID;
float yawKp = 1.0;

float rollAngleF = 0;
float pitchAngleF = 0;
unsigned long lastIMUTime = 0;

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
  delay(3000);  // keep drone still

  Serial.begin(115200);

  pinMode(PPM_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PPM_PIN), ppmISR, RISING);

  for (int i = 0; i < CHANNELS; i++) ppm[i] = 1500;
  ppm[2] = 1000;
  ppm[3] = 1500;

  Wire.begin();
  mpu.initialize();
  mpu.setXAccelOffset(-181);
  mpu.setYAccelOffset(-312);
  mpu.setZAccelOffset(31468);

  mpu.setXGyroOffset(109);
  mpu.setYGyroOffset(280);
  mpu.setZGyroOffset(322);

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

  rollI = pitchI = 0;
  rollAngleF = pitchAngleF = 0;
  lastIMUTime = micros();
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

  float rollRate  = gx / 131.0;
  float pitchRate = gy / 131.0;

  // ---------- COMPLEMENTARY FILTER ----------
  unsigned long now = micros();
  float dt = (now - lastIMUTime) * 1e-6;
  lastIMUTime = now;

  // Safety for first run
  if (dt <= 0 || dt > 0.02) dt = 0.005;

  // Accelerometer angles
  float rollAcc  = atan2(ay, az) * 57.3;
  float pitchAcc = atan2(-ax, az) * 57.3;

  rollAngleF  = 0.98 * (rollAngleF  + rollRate  * dt) + 0.02 * rollAcc;
  pitchAngleF = 0.98 * (pitchAngleF + pitchRate * dt) + 0.02 * pitchAcc;

  // Use filtered angles
  float rollAngle  = rollAngleF;
  float pitchAngle = pitchAngleF;

  // Debug print
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 100) {
    Serial.print("Roll: ");
    Serial.print(rollAngle);
    Serial.print("  Pitch: ");
    Serial.println(pitchAngle);
    lastPrint = millis();
  }

  // Targets
  float rollTarget  = map(rollIn, 1000, 2000, -20, 20);
  float pitchTarget = map(pitchIn, 1000, 2000, -20, 20);

  // PID
  rollError  = rollTarget  - rollAngle;
  pitchError = pitchTarget - pitchAngle;

  if (throttleIn > PID_THROTTLE_CUTOFF) {
  rollI  += rollError;
  pitchI += pitchError;

  rollI  = constrain(rollI,  -300, 300);
  pitchI = constrain(pitchI, -300, 300);

  rollPID  = kp * rollError  + ki * rollI  - kd * rollRate;
  pitchPID = kp * pitchError + ki * pitchI - kd * pitchRate;
  } else {
  rollI = pitchI = 0;
  rollPID = pitchPID = 0;
  }

  rollPID  = constrain(rollPID,  -200, 200);
  pitchPID = constrain(pitchPID, -200, 200);

  lastRollError  = rollError;
  lastPitchError = pitchError;

// YAW CONTROL
yawRate = gz / 131.0;  // gyro Z
float yawTarget = map(yawIn, 1000, 2000, -150, 150);
yawError = yawTarget - yawRate;
yawPID = yawKp * yawError;
yawPID = constrain(yawPID, -200, 200);


  // MOTOR MIX
  if (!armed) {
    writeMotors(MIN_THROTTLE);
  } else {

    int base = (throttleIn < 1050) ? IDLE_THROTTLE :
               constrain(throttleIn, IDLE_THROTTLE, MAX_THROTTLE);

    // m1.writeMicroseconds(constrain(base - rollPID + pitchPID, IDLE_THROTTLE, 2000));
    // m2.writeMicroseconds(constrain(base - rollPID - pitchPID, IDLE_THROTTLE, 2000));
    // m3.writeMicroseconds(constrain(base + rollPID - pitchPID, IDLE_THROTTLE, 2000));
    // m4.writeMicroseconds(constrain(base + rollPID + pitchPID, IDLE_THROTTLE, 2000));

    int m1_out = base - rollPID + pitchPID - yawPID;  // Front Right
    int m2_out = base - rollPID - pitchPID + yawPID;  // Rear Right
    int m3_out = base + rollPID - pitchPID - yawPID;  // Rear Left
    int m4_out = base + rollPID + pitchPID + yawPID;  // Front Left

    m1.writeMicroseconds(constrain(m1_out, IDLE_THROTTLE, 2000));
    m2.writeMicroseconds(constrain(m2_out, IDLE_THROTTLE, 2000));
    m3.writeMicroseconds(constrain(m3_out, IDLE_THROTTLE, 2000));
    m4.writeMicroseconds(constrain(m4_out, IDLE_THROTTLE, 2000));
  }
}
