

// // ===== RC PINS =====
// #define CH_THROTTLE 2   // CH3 from receiver (D2)
// #define CH_STEERING 3   // CH1 D3


// // ===== MOTOR DRIVER 1 (Left Side Motors) =====
// #define IN1_LEFT 4      // LEFT FRONT Motor A
// #define IN2_LEFT 5      // LEFT FRONT Motor B
// #define IN3_LEFT 6      // LEFT BACK Motor A
// #define IN4_LEFT 7      // LEFT BACK Motor B

// // ===== MOTOR DRIVER 2 (Right Side Motors) =====
// #define IN1_RIGHT 8     // RIGHT FRONT Motor A
// #define IN2_RIGHT 9     // RIGHT FRONT Motor B
// #define IN3_RIGHT 10    // RIGHT BACK Motor A
// #define IN4_RIGHT 11    // RIGHT BACK Motor B

// // ===== RC LIMITS =====
// #define THROTTLE_CENTER 1476
// #define THROTTLE_DEAD_ZONE 50

// #define STEERING_CENTER 1441      // Center between 1988 and 994 = ~1441
// #define STEERING_DEAD_ZONE 100    // Wider dead zone for stability

// long ch1, ch2;

// void setup() {
//   Serial.begin(9600);

//   pinMode(CH_THROTTLE, INPUT);
//   pinMode(CH_STEERING, INPUT);

//   // Motor Driver 1 pins
//   pinMode(IN1_LEFT, OUTPUT);
//   pinMode(IN2_LEFT, OUTPUT);
//   pinMode(IN3_LEFT, OUTPUT);
//   pinMode(IN4_LEFT, OUTPUT);

//   // Motor Driver 2 pins
//   pinMode(IN1_RIGHT, OUTPUT);
//   pinMode(IN2_RIGHT, OUTPUT);
//   pinMode(IN3_RIGHT, OUTPUT);
//   pinMode(IN4_RIGHT, OUTPUT);

//   stopMotors();
  
//   Serial.println("=== RC Car Started - STEERING WORKING! ===");
//   Serial.println("Steering: LEFT=994, CENTER=1441, RIGHT=1988");
// }

// void loop() {

//   ch1 = pulseIn(CH_THROTTLE, HIGH, 25000);   // throttle (CH3)
//   ch2 = pulseIn(CH_STEERING, HIGH, 25000);   // steering (CH1) on A0

//   // Debug
//   Serial.print("Throttle: ");
//   Serial.print(ch1);
//   Serial.print("  Steering: ");
//   Serial.print(ch2);
//   Serial.print("  → ");


//   // SIGNAL LOST
//   if (ch1 < 900 || ch1 > 2100) {
//     stopMotors();
//     Serial.println("⚠️ NO SIGNAL!");
//     delay(100);
//     return;
//   }

//   // ================= FORWARD (Throttle UP > 1526) =================
//   if (ch1 > (THROTTLE_CENTER + THROTTLE_DEAD_ZONE)) {

//     resetMotors();
//     delay(5);

//     Serial.print("FORWARD ");

//     // TURN RIGHT (steering > 1541)
//     if (ch2 > (STEERING_CENTER + STEERING_DEAD_ZONE) && ch2 < 2100) {
//       Serial.println("RIGHT");
//       motorLeftForward();
//       motorRightStop();
//     }
//     // TURN LEFT (steering < 1341)
//     else if (ch2 < (STEERING_CENTER - STEERING_DEAD_ZONE) && ch2 > 900) {
//       Serial.println("LEFT");
//       motorRightForward();
//       motorLeftStop();
//     }
//     // STRAIGHT
//     else {
//       Serial.println("STRAIGHT");
//       motorLeftForward();
//       motorRightForward();
//     }
//   }

//   // ================= REVERSE (Throttle DOWN < 1426) =================
//   else if (ch1 < (THROTTLE_CENTER - THROTTLE_DEAD_ZONE)) {

//     resetMotors();
//     delay(5);

//     Serial.print("REVERSE ");

//     // TURN RIGHT (steering > 1541)
//     if (ch2 > (STEERING_CENTER + STEERING_DEAD_ZONE) && ch2 < 2100) {
//       Serial.println("RIGHT");
//       motorLeftReverse();
//       motorRightStop();
//     }
//     // TURN LEFT (steering < 1341)
//     else if (ch2 < (STEERING_CENTER - STEERING_DEAD_ZONE) && ch2 > 900) {
//       Serial.println("LEFT");
//       motorRightReverse();
//       motorLeftStop();
//     }
//     // STRAIGHT
//     else {
//       Serial.println("STRAIGHT");
//       motorLeftReverse();
//       motorRightReverse();
//     }
//   }

//   // ================= NEUTRAL (1426-1526) =================
//   else {
//     resetMotors();
//     Serial.println("STOP");
//   }
  
//   delay(50);
// }

// // ===== LEFT SIDE MOTOR FUNCTIONS (YOUR WORKING LOGIC) =====
// void motorLeftForward() {
//   // LEFT FRONT Motor - Normal
//   digitalWrite(IN1_LEFT, HIGH);
//   digitalWrite(IN2_LEFT, LOW);
  
//   // LEFT BACK Motor - REVERSED
//   digitalWrite(IN3_LEFT, LOW);
//   digitalWrite(IN4_LEFT, HIGH);
// }

// void motorLeftReverse() {
//   // LEFT FRONT Motor - Normal
//   digitalWrite(IN1_LEFT, LOW);
//   digitalWrite(IN2_LEFT, HIGH);
  
//   // LEFT BACK Motor - REVERSED
//   digitalWrite(IN3_LEFT, HIGH);
//   digitalWrite(IN4_LEFT, LOW);
// }

// void motorLeftStop() {
//   digitalWrite(IN1_LEFT, LOW);
//   digitalWrite(IN2_LEFT, LOW);
//   digitalWrite(IN3_LEFT, LOW);
//   digitalWrite(IN4_LEFT, LOW);
// }

// // ===== RIGHT SIDE MOTOR FUNCTIONS (YOUR WORKING LOGIC) =====
// void motorRightForward() {
//   // RIGHT FRONT Motor - Normal
//   digitalWrite(IN1_RIGHT, HIGH);
//   digitalWrite(IN2_RIGHT, LOW);
  
//   // RIGHT BACK Motor - REVERSED
//   digitalWrite(IN3_RIGHT, LOW);
//   digitalWrite(IN4_RIGHT, HIGH);
// }

// void motorRightReverse() {
//   // RIGHT FRONT Motor - Normal
//   digitalWrite(IN1_RIGHT, LOW);
//   digitalWrite(IN2_RIGHT, HIGH);
  
//   // RIGHT BACK Motor - REVERSED
//   digitalWrite(IN3_RIGHT, HIGH);
//   digitalWrite(IN4_RIGHT, LOW);
// }

// void motorRightStop() {
//   digitalWrite(IN1_RIGHT, LOW);
//   digitalWrite(IN2_RIGHT, LOW);
//   digitalWrite(IN3_RIGHT, LOW);
//   digitalWrite(IN4_RIGHT, LOW);
// }

// // ===== RESET ALL MOTORS =====
// void resetMotors() {
//   digitalWrite(IN1_LEFT, LOW);
//   digitalWrite(IN2_LEFT, LOW);
//   digitalWrite(IN3_LEFT, LOW);
//   digitalWrite(IN4_LEFT, LOW);
  
//   digitalWrite(IN1_RIGHT, LOW);
//   digitalWrite(IN2_RIGHT, LOW);
//   digitalWrite(IN3_RIGHT, LOW);
//   digitalWrite(IN4_RIGHT, LOW);
// }

// void stopMotors() {
//   motorLeftStop();
//   motorRightStop();
// }





// // #define STEERING_PIN 3   // CH1
// // #define THROTTLE_PIN 2   // CH2

// // void setup() {
// //   Serial.begin(9600);
// //   pinMode(STEERING_PIN, INPUT);
// //   pinMode(THROTTLE_PIN, INPUT);
// // }

// // void loop() {
// //   long steer = pulseIn(STEERING_PIN, HIGH, 25000);
// //   long thr   = pulseIn(THROTTLE_PIN, HIGH, 25000);

// //   Serial.print("THR: ");
// //   Serial.print(thr);
// //   Serial.print("  STR: ");
// //   Serial.println(steer);

// //   delay(200);
// // }






// // ===== RC PINS =====
// #define CH_THROTTLE 2   // CH3 → D2
// #define CH_STEERING 3   // CH1 → D3

// // ===== MOTOR DRIVER PINS =====
// // LEFT
// #define IN1_LEFT 4
// #define IN2_LEFT 6
// #define IN3_LEFT 7
// #define IN4_LEFT 8

// // RIGHT
// #define IN1_RIGHT 9
// #define IN2_RIGHT 10
// #define IN3_RIGHT 12
// #define IN4_RIGHT A0   // instead of 13


// // ===== RC CALIBRATION =====
// #define THR_MIN 900
// #define THR_MAX 2100
// #define STR_MIN 900
// #define STR_MAX 2100

// #define THR_CENTER 1476
// #define STR_CENTER 1441

// #define THR_DEAD 50
// #define STR_DEAD 100

// long throttle = THR_CENTER;
// long steering = STR_CENTER;

// // ================= SAFE CHANNEL READ =================
// long readChannel(uint8_t pin, long lastValue) {
//   long v = pulseIn(pin, HIGH, 25000);
//   if (v < 900 || v > 2100) return lastValue;
//   return v;
// }

// void setup() {
//   Serial.begin(9600);

//   pinMode(CH_THROTTLE, INPUT);
//   pinMode(CH_STEERING, INPUT);

//   pinMode(IN1_LEFT, OUTPUT);
//   pinMode(IN2_LEFT, OUTPUT);
//   pinMode(IN3_LEFT, OUTPUT);
//   pinMode(IN4_LEFT, OUTPUT);

//   pinMode(IN1_RIGHT, OUTPUT);
//   pinMode(IN2_RIGHT, OUTPUT);
//   pinMode(IN3_RIGHT, OUTPUT);
//   pinMode(IN4_RIGHT, OUTPUT);


//   stopMotors();

//   Serial.println("=== RC CAR READY ===");
// }

// void loop() {

//   // Read RC safely
//   throttle = readChannel(CH_THROTTLE, throttle);
//   steering = readChannel(CH_STEERING, steering);

//   Serial.print("THR: ");
//   Serial.print(throttle);
//   Serial.print("  STR: ");
//   Serial.println(steering);

//   // ================= NEUTRAL =================
//   if (abs(throttle - THR_CENTER) < THR_DEAD) {
//     stopMotors();
//     return;
//   }

//   bool forward = throttle > THR_CENTER;
//   bool leftTurn  = steering < (STR_CENTER - STR_DEAD);
//   bool rightTurn = steering > (STR_CENTER + STR_DEAD);

//   resetMotors();

//   // ================= FORWARD =================
//   if (forward) {
//     if (leftTurn) {
//       motorRightForward();
//     } 
//     else if (rightTurn) {
//       motorLeftForward();
//     } 
//     else {
//       motorLeftForward();
//       motorRightForward();
//     }
//   }

//   // ================= REVERSE =================
//   else {
//     if (leftTurn) {
//       motorRightReverse();
//     } 
//     else if (rightTurn) {
//       motorLeftReverse();
//     } 
//     else {
//       motorLeftReverse();
//       motorRightReverse();
//     }
//   }
// }

// // ================= MOTOR FUNCTIONS =================
// void motorLeftForward() {
//   digitalWrite(IN1_LEFT, HIGH);
//   digitalWrite(IN2_LEFT, LOW);
//   digitalWrite(IN3_LEFT, LOW);
//   digitalWrite(IN4_LEFT, HIGH);
// }

// void motorLeftReverse() {
//   digitalWrite(IN1_LEFT, LOW);
//   digitalWrite(IN2_LEFT, HIGH);
//   digitalWrite(IN3_LEFT, HIGH);
//   digitalWrite(IN4_LEFT, LOW);
// }

// void motorRightForward() {
//   digitalWrite(IN1_RIGHT, HIGH);
//   digitalWrite(IN2_RIGHT, LOW);
//   digitalWrite(IN3_RIGHT, LOW);
//   digitalWrite(IN4_RIGHT, HIGH);
// }

// void motorRightReverse() {
//   digitalWrite(IN1_RIGHT, LOW);
//   digitalWrite(IN2_RIGHT, HIGH);
//   digitalWrite(IN3_RIGHT, HIGH);
//   digitalWrite(IN4_RIGHT, LOW);
// }

// void resetMotors() {
//   digitalWrite(IN1_LEFT, LOW);
//   digitalWrite(IN2_LEFT, LOW);
//   digitalWrite(IN3_LEFT, LOW);
//   digitalWrite(IN4_LEFT, LOW);

//   digitalWrite(IN1_RIGHT, LOW);
//   digitalWrite(IN2_RIGHT, LOW);
//   digitalWrite(IN3_RIGHT, LOW);
//   digitalWrite(IN4_RIGHT, LOW);
// }

// void stopMotors() {
//   resetMotors();
// }







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

