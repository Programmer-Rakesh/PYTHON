#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "UnoR4_Network";
const char* password = "password123";
WiFiUDP udp;
const unsigned int localPort = 12345;

#define IN1  25
#define IN2  26
#define IN3  27
#define IN4  14
#define ENA  32
#define ENB  33
int motorSpeed = 120;

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void forward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}

void turnLeft() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}

void turnRight() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, motorSpeed);
  analogWrite(ENB, motorSpeed);
}


void setup() {
  Serial.begin(115200);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  stopMotors();

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  udp.begin(localPort);
}

void loop() {
  int packetLen = udp.parsePacket();
  if (packetLen > 0) {
    unsigned long receiveTime = millis();
    if (packetLen == 1 || packetLen == 2) {
      char incomingPacket[3];
      int len = udp.read(incomingPacket, packetLen);
      incomingPacket[len] = 0;

      Serial.print("Received: ");
      Serial.print(incomingPacket);
      Serial.print(" at ");
      Serial.println(receiveTime);

      if (strcmp(incomingPacket, "01") == 0 || incomingPacket[0] == '0' || incomingPacket[0] == '1' || 
          incomingPacket[0] == '2' || incomingPacket[0] == '3') {
        if (incomingPacket[0] == '2') turnLeft();
        else if (incomingPacket[0] == '3') turnRight();
        else if (incomingPacket[0] == '1' || strcmp(incomingPacket, "01") == 0) forward();
        else if (incomingPacket[0] == '0') stopMotors();

      }
    }
  }
}