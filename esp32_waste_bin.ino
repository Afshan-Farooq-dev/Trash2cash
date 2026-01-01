// ================================
//  BIN CONTROL SYSTEM (ESP32 WROOM)
//  Updated for connection with ESP32-CAM
// ================================

#include <WiFi.h>
#include <ESP32Servo.h>
#include <WebServer.h>

// ===================================
// 1. SERVO CONFIGURATION
// ===================================
Servo servoPan;   // Horizontal servo
Servo servoTilt;  // Vertical servo

int panPin = 13;   // Servo 1
int tiltPin = 33;  // Servo 2

int neutralPan = 90;
int neutralTilt = 70;

// ===================================
// 2. MOTOR DRIVER CONFIGURATION
// ===================================
int IN1 = 26;
int IN2 = 27;
int IN3 = 14;
int IN4 = 12;

// ===================================
// 3. WIFI & SERVER CONFIGURATION
// ===================================
// NOTE: this ESP32-WROOM will connect to ESP32-CAM’s WiFi (BinCam)
const char* ssid = "BinCam";
const char* password = "012345678";

WebServer server(80);

// ===================================
// 4. SERVO MOVEMENT FUNCTIONS
// ===================================
void moveServoSlow(Servo &servo, int start, int end, int delayTime) {
  int step = (end > start) ? 1 : -1;
  for (int pos = start; pos != end; pos += step) {
    servo.write(pos);
    delay(delayTime);
  }
  servo.write(end);
}

void resetToNeutral() {
  Serial.println("Returning to neutral...");
  moveServoSlow(servoTilt, servoTilt.read(), neutralTilt, 15);
  delay(300);
  moveServoSlow(servoPan, servoPan.read(), neutralPan, 15);
  delay(1000);
  Serial.println("✅ Back to neutral position!");
}

// ===================================
// 5. MOTOR CONTROL FUNCTIONS
// ===================================
void motor1Forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
}

void motor1Reverse() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
}

void motor1Stop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}

void motor2Forward() {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void motor2Reverse() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void motor2Stop() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

// ===================================
// 6. API HANDLERS
// ===================================
void handleRoot() {
  String message = "ESP32 WROOM Connected to BinCam.\nTry /paper, /plastic, /openlid, /closelid";
  server.send(200, "text/plain", message);
}

void handlePaper() {
  Serial.println("🧾 Paper detected!");
  moveServoSlow(servoPan, servoPan.read(), 90, 15);
  delay(300);
  moveServoSlow(servoTilt, servoTilt.read(), 20, 15);
  delay(5000);
  resetToNeutral();
  server.send(200, "text/plain", "Paper sorted!");
}

void handlePlastic() {
  Serial.println("🧃 Plastic detected!");
  moveServoSlow(servoPan, servoPan.read(), 180, 15);
  delay(300);
  moveServoSlow(servoTilt, servoTilt.read(), 20, 15);
  delay(5000);
  resetToNeutral();
  server.send(200, "text/plain", "Plastic sorted!");
}

void handleGlass() {
  Serial.println("🧴 Glass detected!");
  moveServoSlow(servoPan, servoPan.read(), 90, 15);
  delay(300);
  moveServoSlow(servoTilt, servoTilt.read(), 130, 15);
  delay(5000);
  resetToNeutral();
  server.send(200, "text/plain", "Glass sorted!");
}

void handleMetal() {
  Serial.println("🧲 Metal detected!");
  moveServoSlow(servoPan, servoPan.read(), 180, 15);
  delay(300);
  moveServoSlow(servoTilt, servoTilt.read(), 130, 15);
  delay(5000);
  resetToNeutral();
  server.send(200, "text/plain", "Metal sorted!");
}

void handleOpenLid() {
  Serial.println("🚪 Lid Opening...");
  motor1Forward();
  motor2Forward();
  delay(400);  // increased timing (was 200ms → now 400ms)
  motor1Stop();
  motor2Stop();
  server.send(200, "text/plain", "Lid Opened!");
}

void handleCloseLid() {
  Serial.println("🚪 Lid Closing...");
  motor1Reverse();
  motor2Reverse();
  delay(400);  // increased timing (was 200ms → now 400ms)
  motor1Stop();
  motor2Stop();
  server.send(200, "text/plain", "Lid Closed!");
}

// ===================================
// 7. SETUP
// ===================================
void setup() {
  Serial.begin(115200);
  Serial.println("Booting BinCam WROOM Controller...");

  // Connect to ESP32-CAM Wi-Fi
  WiFi.begin(ssid, password);
  WiFi.config(IPAddress(192, 168, 4, 81), IPAddress(192, 168, 4, 1), IPAddress(255, 255, 255, 0));  // static IP
  Serial.print("Connecting to "); Serial.println(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ Connected to BinCam network!");
  Serial.print("WROOM IP Address: ");
  Serial.println(WiFi.localIP());

  // Servo setup
  servoPan.attach(panPin);
  servoTilt.attach(tiltPin);
  servoPan.write(neutralPan);
  servoTilt.write(neutralTilt);

  // Motor driver setup
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  motor1Stop();
  motor2Stop();

  // Web routes
  server.on("/", handleRoot);
  server.on("/paper", handlePaper);
  server.on("/plastic", handlePlastic);
  server.on("/glass", handleGlass);
  server.on("/metal", handleMetal);
  server.on("/openlid", handleOpenLid);
  server.on("/closelid", handleCloseLid);

  server.begin();
  Serial.println("✅ Web Server Ready! Try http://192.168.4.81/");
}

// ===================================
// 8. LOOP
// ===================================
void loop() {
  server.handleClient();
}