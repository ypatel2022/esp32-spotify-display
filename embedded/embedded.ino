#include "env.h"

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1351.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <WiFi.h>

// screen size definitions
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 128

// display pin configuration
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

Adafruit_SSD1351 oledDisplay(SCREEN_WIDTH, SCREEN_HEIGHT, CS_PIN, DC_PIN, MOSI_PIN, SCLK_PIN, RST_PIN);

// how frequently to make a call to the server (in miliseconds)
unsigned long timerDelay = 10000;
unsigned long lastTime = 0;

// will store the image bitmap array
uint16_t albumCover[16384] PROGMEM;

void setup()
{
    Serial.begin(115200);

    // connect to wifi
    WiFi.begin(WIFI_SSID, PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(500);
    }
    Serial.println("");

    // initialize display
    oledDisplay.begin();
    Serial.println("Initialized OLED display");

    // initially clear display
    oledDisplay.drawRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK);
}

void loop()
{
    if ((millis() - lastTime) > timerDelay)
    {
        // check if we're connected to the internet
        if (WiFi.status() == WL_CONNECTED)
        {
            WiFiClient client;
            HTTPClient http;

            // Send request
            http.useHTTP10(true);
            http.begin(client, SERVER_IP);
            http.GET();

            // create a stream
            WiFiClient *stream = http.getStreamPtr();

            // used for no-song checking scenario
            bool cleared = false;

            // for reading in stream and converting to bitmap array
            String buff = "";
            int cc = 0;
            int n = 0;

            while (stream->available())
            {
                // the first 15 characters are generally useless for the bitmap data
                // however, we must check if key is no-song, which lets us know to break out of loop
                if (cc < 15)
                {
                    // store into buffer to check if no song
                    buff += stream->read();
                    cc++;

                    if (buff == "{\n  \"no-song")
                    {
                        break;
                    }

                    continue;
                }
                else if (cleared == false)
                {
                    // if there is a song, must clear buffer and make sure not to clear it again
                    buff = "";
                    cleared = true;
                }

                // get character
                char c = stream->read();

                // if its a comma, we know the whole number
                if (c == ',')
                {
                    // conver the number in the buffer to 16 bit uint
                    albumCover[n] = (uint16_t)buff.toInt();
                    // increment index variable for the bitmap array
                    n++;
                    // clear buffer
                    buff = "";
                }
                else if (c == ']')
                {
                    // break out of loop if at the end
                    break;
                }
                else
                {
                    // otherwise add char to buffer
                    buff += c;
                }

                // counter for keeping track of how many characters we have read in
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

        Serial.println('Updating display...');
        oledDisplay.drawRGBBitmap(0, 0, albumCover, SCREEN_WIDTH, SCREEN_HEIGHT);
    }
}