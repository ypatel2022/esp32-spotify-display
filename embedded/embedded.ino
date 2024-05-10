#include "env.h"
#include "utils.h"

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1351.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <WiFi.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 128

// You can use any (4 or) 5 pins
#define SCLK_PIN 18
#define MOSI_PIN 23
#define DC_PIN 17
#define CS_PIN 5
#define RST_PIN 4

// Color definitions
#define BLACK 0x0000
#define BLUE 0x001F
#define RED 0xF800
#define GREEN 0x07E0
#define CYAN 0x07FF
#define MAGENTA 0xF81F
#define YELLOW 0xFFE0
#define WHITE 0xFFFF

Adafruit_SSD1351 tft = Adafruit_SSD1351(SCREEN_WIDTH, SCREEN_HEIGHT, CS_PIN, DC_PIN, MOSI_PIN, SCLK_PIN, RST_PIN);

unsigned long lastTime = 0;
unsigned long timerDelay = 10000;

uint16_t albumCover[16384] PROGMEM;
String jsonResponse;
String httpGETRequest(const char *serverName);

String payload;
String ServerPath = SERVER_IP;
int httpResponseCode = 0;

void setup()
{
    Serial.begin(115200);

    WiFi.begin(WIFI_SSID, PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(500);
    }
    Serial.println("");

    tft.begin();
    Serial.println("initialized oled.");

    tft.drawRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK);
}

void loop()
{
    if ((millis() - lastTime) > timerDelay)
    {
        // check if we're connected to the internet
        if (WiFi.status() == WL_CONNECTED)
        {
            WiFiClient client; // or WiFiClientSecure for HTTPS
            HTTPClient http;

            // Send request
            http.useHTTP10(true);
            http.begin(client, SERVER_IP);
            http.GET();

            // String payload = http.getString();
            WiFiClient *stream = http.getStreamPtr();
            // String payload = "";

            String buff = "";
            int cc = 0;
            int n = 0;
            while (stream->available())
            {
                if (cc < 15)
                {
                    cc++;
                    continue;
                }

                char c = stream->read();

                if (c == ',')
                {
                    albumCover[n] = (uint16_t)buff.toInt();
                    n++;
                    buff = "";
                }
                else if (c == ']')
                {
                    break;
                }
                else
                {
                    buff += c;
                }

                cc++;
            }

            // Disconnect
            http.end();
        }
        else
        {
            Serial.println("Not connected to WiFi");
        }

        lastTime = millis();

        Serial.println('updating display....');
        tft.drawRGBBitmap(0, 0, albumCover, SCREEN_WIDTH, SCREEN_HEIGHT);
    }
}