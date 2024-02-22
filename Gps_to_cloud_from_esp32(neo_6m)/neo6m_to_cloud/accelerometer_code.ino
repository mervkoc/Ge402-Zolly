
#include <Wire.h>

const int ADXL345 = 0x53; // The ADXL345 sensor I2C address
float X_out, Y_out, Z_out;
int steps = 0;
float lastX = 0, lastY = 0;
const float stepThresholdX = 0.8; // Threshold for step detection in X-axis
const float stepThresholdY = 0.8; // Threshold for step detection in Y-axis

void setup() {
  Serial.begin(9600);
  Wire.begin(11, 12); // Initialize I2C communication
  // Set ADXL345 in measuring mode
  Wire.beginTransmission(ADXL345);
  Wire.write(0x2D); // Access POWER_CTL Register
  Wire.write(8); // Bit D3 High for measurement mode
  Wire.endTransmission();
  delay(10);
}

void loop() {
  // Read accelerometer data
  Wire.beginTransmission(ADXL345);
  Wire.write(0x32); // ACCEL_XOUT_H register
  Wire.endTransmission(false);
  Wire.requestFrom(ADXL345, 6, true); // Request 6 bytes from the ADXL345
  
  X_out = (Wire.read() | Wire.read() << 8) / 256.0;
  Y_out = (Wire.read() | Wire.read() << 8) / 256.0;
  Z_out = (Wire.read() | Wire.read() << 8) / 256.0;
  
  // Step detection based on X and Y axis
  if (abs(X_out - lastX) > stepThresholdX || abs(Y_out - lastY) > stepThresholdY) {
    steps++;
    Serial.print("Step Detected. Total Steps: ");
    Serial.println(steps)/256;
    Serial.println(stepThresholdX);


  }
  
  lastX = X_out;
  lastY = Y_out;
  
  Serial.print("Xa= ");
  Serial.print(X_out);
  Serial.print("   Ya= ");
  Serial.print(Y_out);
  Serial.print("   Za= ");
  Serial.println(Z_out);
  
  delay(100); // Delay for readability
}

