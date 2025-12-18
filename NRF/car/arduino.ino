#include <SPI.h>
#include <RF24.h>

#define CE_PIN 2    // ✅ Your pins unchanged
#define CSN_PIN 3   // ✅ Your pins unchanged

RF24 radio(CE_PIN, CSN_PIN);
const byte address[6] = "CAR01";

// ===== Motor Pins (YOUR CONFIGURATION) =====
// Left motors
#define A1_IN1 A0
#define A1_IN2 A1
#define A2_IN1 A2
#define A2_IN2 A3

// Right motors
#define B1_IN1 A4
#define B1_IN2 A5
#define B2_IN1 4
#define B2_IN2 5

// ===== RF DATA STRUCT (MUST MATCH PYTHON <hh>) =====
struct DataPacket {
  int16_t x;   // left / right  (-100 to 100)
  int16_t y;   // forward / backward (-100 to 100)
};

DataPacket data;

// ===== SAFETY =====
unsigned long lastReceiveTime = 0;
#define TIMEOUT 500   // ms

// ===== Motor Functions =====
void stopMotors() {
  digitalWrite(A1_IN1, LOW);
  digitalWrite(A1_IN2, LOW);
  digitalWrite(A2_IN1, LOW);
  digitalWrite(A2_IN2, LOW);
  digitalWrite(B1_IN1, LOW);
  digitalWrite(B1_IN2, LOW);
  digitalWrite(B2_IN1, LOW);
  digitalWrite(B2_IN2, LOW);
}

void moveForward() {
  // All motors forward
  digitalWrite(A1_IN1, HIGH);
  digitalWrite(A1_IN2, LOW);
  digitalWrite(A2_IN1, HIGH);
  digitalWrite(A2_IN2, LOW);
  digitalWrite(B1_IN1, HIGH);
  digitalWrite(B1_IN2, LOW);
  digitalWrite(B2_IN1, HIGH);
  digitalWrite(B2_IN2, LOW);
}

void moveBackward() {
  // All motors backward
  digitalWrite(A1_IN1, LOW);
  digitalWrite(A1_IN2, HIGH);
  digitalWrite(A2_IN1, LOW);
  digitalWrite(A2_IN2, HIGH);
  digitalWrite(B1_IN1, LOW);
  digitalWrite(B1_IN2, HIGH);
  digitalWrite(B2_IN1, LOW);
  digitalWrite(B2_IN2, HIGH);
}

void turnLeft() {
  // Right motors forward, left motors stop (or reverse for tighter turn)
  digitalWrite(A1_IN1, LOW);
  digitalWrite(A1_IN2, LOW);
  digitalWrite(A2_IN1, LOW);
  digitalWrite(A2_IN2, LOW);
  digitalWrite(B1_IN1, HIGH);
  digitalWrite(B1_IN2, LOW);
  digitalWrite(B2_IN1, HIGH);
  digitalWrite(B2_IN2, LOW);
}

void turnRight() {
  // Left motors forward, right motors stop (or reverse for tighter turn)
  digitalWrite(A1_IN1, HIGH);
  digitalWrite(A1_IN2, LOW);
  digitalWrite(A2_IN1, HIGH);
  digitalWrite(A2_IN2, LOW);
  digitalWrite(B1_IN1, LOW);
  digitalWrite(B1_IN2, LOW);
  digitalWrite(B2_IN1, LOW);
  digitalWrite(B2_IN2, LOW);
}

void setup() {
  Serial.begin(9600);
  Serial.println("=== RC Car Receiver Starting ===");

  // Motor pins as OUTPUT
  pinMode(A1_IN1, OUTPUT);
  pinMode(A1_IN2, OUTPUT);
  pinMode(A2_IN1, OUTPUT);
  pinMode(A2_IN2, OUTPUT);
  pinMode(B1_IN1, OUTPUT);
  pinMode(B1_IN2, OUTPUT);
  pinMode(B2_IN1, OUTPUT);
  pinMode(B2_IN2, OUTPUT);

  stopMotors();

  // ===== RF SETUP =====
  if (!radio.begin()) {
    Serial.println("❌ Radio hardware not responding!");
    while (1);  // Hold program in infinite loop
  }
  
  radio.setChannel(108);
  radio.setPayloadSize(4);  // ✅ CRITICAL: Must be 4 bytes
  radio.openReadingPipe(1, address);
  radio.startListening();

  Serial.println("✅ Receiver ready!");
  Serial.print("Payload size: ");
  Serial.print(sizeof(DataPacket));
  Serial.println(" bytes");
  
  lastReceiveTime = millis();
}

void loop() {
  if (radio.available()) {
    radio.read(&data, sizeof(data));

    Serial.print("📡 X: ");
    Serial.print(data.x);
    Serial.print("  Y: ");
    Serial.println(data.y);

    lastReceiveTime = millis();
    stopMotors();  // Stop first to prevent overlapping commands

    // ===== CONTROL LOGIC =====
    if (data.y > 50) {
      Serial.println("⬆️ Forward");
      moveForward();
    }
    else if (data.y < -50) {
      Serial.println("⬇️ Backward");
      moveBackward();
    }
    else if (data.x > 50) {
      Serial.println("➡️ Right");
      turnRight();
    }
    else if (data.x < -50) {
      Serial.println("⬅️ Left");
      turnLeft();
    }
    else {
      Serial.println("⏸️ Stop");
      stopMotors();
    }
  }

  // ===== FAILSAFE: Stop if no signal =====
  if (millis() - lastReceiveTime > TIMEOUT) {
    stopMotors();
  }

  delay(10);
}