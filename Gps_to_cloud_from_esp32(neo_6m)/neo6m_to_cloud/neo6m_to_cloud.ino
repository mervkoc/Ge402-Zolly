#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPS++.h>
#include <HardwareSerial.h>
#include <TinyGPS++.h>

const char* ssid = "bilkent-EEE";

const char* firestoreURL = "https://firestore.googleapis.com/v1/projects/zollyapp/databases/(default)/documents/your_collection/your_document?key=AIzaSyCCmaLQVfUrt_iyv6sM4TsCi14tBhCGB_Q";
const char *cloudFunctionURL = "https://europe-west6-zollyapp.cloudfunctions.net/function-1";


WiFiClient client;
TinyGPSPlus gps;
HardwareSerial gpsSerial(1); // Use UART1 for GPS


void setup() {
  Serial.begin(115200);
  gpsSerial.begin(9600, SERIAL_8N1, 17, -1); // Start GPS serial communication; TX pin is not used, so -1
  Serial.println("GPS Receiver Test");
  WiFi.begin(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  while (gpsSerial.available() > 0) {
    char c = gpsSerial.read();
    if (gps.encode(c)) {
      if (gps.location.isValid()) {
        String latitudeStr = String(gps.location.lat(), 6);
        String longitudeStr = String(gps.location.lng(), 6);

        String gpsData = "{\"latitude\":" + latitudeStr + ",\"longitude\":" + longitudeStr + "}";
        sendGPSDataToCloud(gpsData);
        Serial.print("Latitude: ");
        Serial.println(latitudeStr);
        Serial.print("Longitude: ");
        Serial.println(longitudeStr);
      }else {
        Serial.println("Waiting for GPS signal...");
      }
    
  }
}
}

void sendGPSDataToCloud(String data) {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(cloudFunctionURL);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(data);

    if (httpResponseCode == 200) { // Checking for HTTP status 200 OK
      Serial.println("Successfully uploaded to cloud!");
    }
    else {
      Serial.print("Upload failed with HTTP response code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
  delay(10000); // Adjust based on how often you want to send data
}







