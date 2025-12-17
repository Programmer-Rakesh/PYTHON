// #include <SPI.h>
// #include <RF24.h>

// #define CE_PIN 2
// #define CSN_PIN 3

// RF24 radio(CE_PIN, CSN_PIN);
// const byte address[6] = "CAR01";

// // ===== Motor Pins =====
// // Left motors
// #define A1_IN1 A0
// #define A1_IN2 A1
// #define A2_IN1 A2
// #define A2_IN2 A3

// // Right motors
// #define B1_IN1 A4
// #define B1_IN2 A5
// #define B2_IN1 4
// #define B2_IN2 5

// struct DataPacket {
//   int x;   // left / right
//   int y;   // forward / backward
// };

// DataPacket data;

// if (radio.available()) {
//   radio.read(&data, sizeof(data));

//   Serial.println("DATA RECEIVED");
//   Serial.print("X: ");
//   Serial.print(data.x);
//   Serial.print(" Y: ");
//   Serial.println(data.y);
// }


// // ===== Motor Functions =====
// void stopMotors() {
//   digitalWrite(A1_IN1, LOW);
//   digitalWrite(A1_IN2, LOW);
//   digitalWrite(A2_IN1, LOW);
//   digitalWrite(A2_IN2, LOW);
//   digitalWrite(B1_IN1, LOW);
//   digitalWrite(B1_IN2, LOW);
//   digitalWrite(B2_IN1, LOW);
//   digitalWrite(B2_IN2, LOW);
// }

// void moveForward() {
//   digitalWrite(A1_IN1, HIGH);
//   digitalWrite(A2_IN1, HIGH);
//   digitalWrite(B1_IN1, HIGH);
//   digitalWrite(B2_IN1, HIGH);
// }

// void moveBackward() {
//   digitalWrite(A1_IN2, HIGH);
//   digitalWrite(A2_IN2, HIGH);
//   digitalWrite(B1_IN2, HIGH);
//   digitalWrite(B2_IN2, HIGH);
// }

// void turnLeft() {
//   digitalWrite(B1_IN1, HIGH);
//   digitalWrite(B2_IN1, HIGH);
// }

// void turnRight() {
//   digitalWrite(A1_IN1, HIGH);
//   digitalWrite(A2_IN1, HIGH);
// }

// void setup() {
//   // 🔹 Start Serial
//   Serial.begin(9600);
//   Serial.println("Receiver ready, waiting for data...");

//   // Motor pins
//   pinMode(A1_IN1, OUTPUT);
//   pinMode(A1_IN2, OUTPUT);
//   pinMode(A2_IN1, OUTPUT);
//   pinMode(A2_IN2, OUTPUT);
//   pinMode(B1_IN1, OUTPUT);
//   pinMode(B1_IN2, OUTPUT);
//   pinMode(B2_IN1, OUTPUT);
//   pinMode(B2_IN2, OUTPUT);

//   stopMotors();

//   // RF setup
//   radio.begin();
//   radio.setPALevel(RF24_PA_MAX);
//   radio.setChannel(108);
//   radio.openReadingPipe(1, address);
//   radio.startListening();

//   lastReceiveTime = millis();
// }

// void loop() {
//   if (radio.available()) {
//     Serial.println("DATA RECEIVED");

//     radio.read(&data, sizeof(data));

//     Serial.print("X: ");
//     Serial.print(data.x);
//     Serial.print("  Y: ");
//     Serial.println(data.y);

//     lastReceiveTime = millis();
//     stopMotors();

//     if (data.y > 5000) {
//       moveForward();
//     }
//     else if (data.y < -5000) {
//       moveBackward();
//     }
//     else if (data.x > 5000) {
//       turnRight();
//     }
//     else if (data.x < -5000) {
//       turnLeft();
//     }
//     else {
//       stopMotors();
//     }
//   }

//   // Safety timeout
//   if (millis() - lastReceiveTime > TIMEOUT) {
//     stopMotors();
//   }

//   delay(10);
// }



#include <SPI.h>
#include <RF24.h>

#define CE_PIN 2
#define CSN_PIN 3

RF24 radio(CE_PIN, CSN_PIN);
const byte address[6] = "CAR01";

// ===== Motor Pins =====
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
  int16_t x;   // left / right
  int16_t y;   // forward / backward
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
  digitalWrite(A1_IN1, HIGH);
  digitalWrite(A2_IN1, HIGH);
  digitalWrite(B1_IN1, HIGH);
  digitalWrite(B2_IN1, HIGH);
}

void moveBackward() {
  digitalWrite(A1_IN2, HIGH);
  digitalWrite(A2_IN2, HIGH);
  digitalWrite(B1_IN2, HIGH);
  digitalWrite(B2_IN2, HIGH);
}

void turnLeft() {
  digitalWrite(B1_IN1, HIGH);
  digitalWrite(B2_IN1, HIGH);
}

void turnRight() {
  digitalWrite(A1_IN1, HIGH);
  digitalWrite(A2_IN1, HIGH);
}

void setup() {
  Serial.begin(9600);
  Serial.println("Receiver ready, waiting for data...");

  // Motor pins
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
  radio.begin();
  radio.setChannel(108);
  radio.setPayloadSize(sizeof(DataPacket));  // 🔥 VERY IMPORTANT
  radio.openReadingPipe(1, address);
  radio.startListening();

  lastReceiveTime = millis();
}

void loop() {
  if (radio.available()) {
    radio.read(&data, sizeof(data));

    Serial.print("X: ");
    Serial.print(data.x);
    Serial.print("  Y: ");
    Serial.println(data.y);

    lastReceiveTime = millis();
    stopMotors();

    // ===== SIMPLE CONTROL =====
    if (data.y > 50) {
      moveForward();
    }
    else if (data.y < -50) {
      moveBackward();
    }
    else if (data.x > 50) {
      turnRight();
    }
    else if (data.x < -50) {
      turnLeft();
    }
    else {
      stopMotors();
    }
  }

  // ===== FAILSAFE =====
  if (millis() - lastReceiveTime > TIMEOUT) {
    stopMotors();
  }

  delay(10);
}
