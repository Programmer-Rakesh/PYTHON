#include "esp_camera.h"
#include <WiFi.h>
#include "esp_http_server.h"

// ================= WIFI =================
const char *ssid = "Airtel_JaiHanuman";
const char *password = "Hanu0009";

// ================= CAMERA PINS =================
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// ================= HTML PAGE =================
static const char PROGMEM HTML_PAGE[] = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>ESP32 CAM</title>
  <style>
    body { text-align:center; font-family:Arial; background:#111; color:white; }
    img { width:90%%; max-width:600px; border-radius:10px; border:2px solid white; }
    .box { margin-top:20px; }
    button {
      padding:10px 20px;
      font-size:16px;
      margin:5px;
      border-radius:8px;
    }
  </style>
</head>
<body>

<h2>ESP32-CAM LIVE STREAM</h2>

<div class="box">
  <img src="/stream">
</div>

</body>
</html>
)rawliteral";

// ================= HANDLERS =================
static esp_err_t index_handler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html");
  return httpd_resp_send(req, HTML_PAGE, strlen(HTML_PAGE));
}

static esp_err_t stream_handler(httpd_req_t *req) {
  camera_fb_t * fb = NULL;
  esp_err_t res = ESP_OK;

  res = httpd_resp_set_type(req,
    "multipart/x-mixed-replace;boundary=frame");

  while (true) {
    fb = esp_camera_fb_get();
    if (!fb) continue;

    httpd_resp_send_chunk(req,
      "--frame\r\nContent-Type: image/jpeg\r\n\r\n", 37);

    httpd_resp_send_chunk(req,
      (const char *)fb->buf, fb->len);

    httpd_resp_send_chunk(req, "\r\n", 2);

    esp_camera_fb_return(fb);
  }

  return res;
}

// ================= SERVER =================
void startCameraServer() {
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  httpd_handle_t server = NULL;

  httpd_start(&server, &config);

  httpd_uri_t index_uri = {
    .uri = "/",
    .method = HTTP_GET,
    .handler = index_handler,
    .user_ctx = NULL
  };

  httpd_uri_t stream_uri = {
    .uri = "/stream",
    .method = HTTP_GET,
    .handler = stream_handler,
    .user_ctx = NULL
  };

  httpd_register_uri_handler(server, &index_uri);
  httpd_register_uri_handler(server, &stream_uri);
}

// ================= SETUP =================
void setup() {
  Serial.begin(115200);
  delay(1000);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;

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

  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;

  config.pin_pwdn  = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;

  config.xclk_freq_hz = 10000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_VGA;   // bigger than QVGA
  config.jpeg_quality = 12;
  config.fb_count = 1;
  config.grab_mode = CAMERA_GRAB_LATEST;

  if (psramFound()) {
    config.fb_count = 2;
    config.jpeg_quality = 10;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed: 0x%x\n", err);
    return;
  }

  Serial.println("Camera OK!");

  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
  Serial.println(WiFi.localIP());

  startCameraServer();

  Serial.println("Open browser and go to IP address");
}

// ================= LOOP =================
void loop() {
  delay(10000);
}