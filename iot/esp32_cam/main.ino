#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend endpoint configuration
const char* backendUrl = "http://192.168.1.100:8000/events/ingest";
const char* deviceToken = "demo-device";

// GPIO configuration
#define PIR_PIN 13
#define RELAY_PIN 12

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_SVGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void loop() {
  int pirState = digitalRead(PIR_PIN);
  if (pirState == HIGH) {
    captureAndSend();
    delay(5000); // Debounce after sending an event
  }
  delay(100);
}

void captureAndSend() {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  if ((WiFi.status() == WL_CONNECTED)) {
    HTTPClient http;
    http.begin(backendUrl);
    http.addHeader("Content-Type", "multipart/form-data; boundary=ESP32CAM");

    String body = "--ESP32CAM\r\n";
    body += "Content-Disposition: form-data; name=\"device_token\"\r\n\r\n";
    body += deviceToken;
    body += "\r\n--ESP32CAM\r\n";
    body += "Content-Disposition: form-data; name=\"image\"; filename=\"capture.jpg\"\r\n";
    body += "Content-Type: image/jpeg\r\n\r\n";

    int contentLength = body.length() + fb->len + strlen("\r\n--ESP32CAM--\r\n");
    http.addHeader("Content-Length", String(contentLength));

    WiFiClient *stream = http.getStreamPtr();
    http.collectHeaders(NULL, 0);

    http.writeToStream((uint8_t*)body.c_str(), body.length());
    stream->write(fb->buf, fb->len);
    http.writeToStream((uint8_t*)"\r\n--ESP32CAM--\r\n", strlen("\r\n--ESP32CAM--\r\n"));

    int statusCode = http.GET();
    if (statusCode > 0) {
      Serial.printf("Backend response: %d\n", statusCode);
      String payload = http.getString();
      Serial.println(payload);
      if (payload.indexOf("unlock") >= 0) {
        digitalWrite(RELAY_PIN, HIGH);
        delay(2000);
        digitalWrite(RELAY_PIN, LOW);
      }
    } else {
      Serial.printf("HTTP error: %s\n", http.errorToString(statusCode).c_str());
    }

    http.end();
  }

  esp_camera_fb_return(fb);
}
