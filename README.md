# ESP32 Spotify Display


This project utilizes an ESP32 module and a small OLED display to showcase the album art of the currently playing song on Spotify.

## Overview

The ESP32 module connects to a Python Flask server which will process the Spotify API data and send it back with a specific format. It will then take the given data and display it on the OLED display in real-time. 


## Requirements
- ESP32 module with WiFi connectivity. I used the [ESP32 WROOM 32](https://www.amazon.ca/ESP-WROOM-32-NodeMCU-Development-Bluetooth-Microcontroller/dp/B0C9VSYS4N).
- A 1.5inch OLED Display. Here are some links: [amazon.ca](https://www.amazon.ca/1-5inch-RGB-OLED-Module-Interface/dp/B07V579YK2), [adafruit.com](https://www.adafruit.com/product/1431).
- Spotify Premium account. You will need this to create a developer account and get API access.
- Arduino IDE or Visual Studio Code with the Arduino extension. You can find many tutorials to set them up to work with the ESP32.


## Setup
1. [Spotify API Tokens](#spotify-api-tokens)
1. [Server Setup](#server-setup)
1. [ESP32 Setup](#esp32-setup)


## Spotify API Tokens
1. Go to https://developer.spotify.com/dashboard
1. Press the "Create app" button
1. Give your app and name and a short description
1. Copy and paste the following url into the "Redirect URI" field: https://alecchen.dev/spotify-refresh-token
1. Check Web API under "Which API/SDKs are you planning to use?"
1. Check the I understand box to accept Spotify's Developer Terms of Service and Design Guidelines
1. Next, press the "Save" button
1. Now, click the "Settings" button
1. Click "View client secret"
1. Save the "Client ID" and "Client secret" somewhere for now, we will need them for the next step and future steps.
1. Open the following website https://alecchen.dev/spotify-refresh-token/
1. Here you will see fields for the Client ID and Client secret, paste them in.
1. Under Scope, select the following options: 'user-read-playback-state', 'user-read-currently-playing'
1. finally, click submit and the page will redirect you to a spotify login and you can click the Agree button.
1. After agreeing, it will take you back to the website and you will see a new field that says 'Refresh Token'. You want to copy this to clipboard and save it for future use.


## Server Setup
1. Clone or download the repository.
1. Open the `server` directory and open `.env.template`
1. Rename the file to `.env`
1. Here you will see fields that will correspond to the Spotify API Tokens we just got. Paste them in after the '=' equal sign in their respective place.
1. Now you can run the server in 2 different ways:
    1. Run using Flask
        - Open terminal in the server directory
        - Install packages using:
        ```bash
        pip install -r requirements.txt
        ```
        - Run the server using:
        ```bash
        flask --app server.py --debug run --host=0.0.0.0
        ```
        - The server should start up and it will tell you IP addresses that the server is running on
        - On the third line of output it will say something like: ` * Running on http://x.x.x.x:5000` where the x's represent any number (this will be random based on your IP address)
        - Copy the IP address `http://x.x.x.x:5000` and save for later use to setup the ESP32
    1. Run using Docker
        - Make sure Docker is running
        - Open a terminal in the server directory
        - Run the server using:
        ```bash
        docker image build -t flask_docker . && docker run -p 5000:5000 -d flask_docker
        ```

## ESP32 Setup

1. Clone or download the repository.
1. Open the `embedded` directory and open `template.env.h`
1. Rename the file to `env.h`
1. Paste your server IP address from earlier into this
1. Also paste in your WiFi name and password into the corresponding fields
1. Open `embedded.ino` inside your Arduino or Visual Studio Code IDE
1. Download and install the following Arduino libraries: Adafruit_GFX, Adafruit_SSD1351, ArduinoJson. You can find tutorials on how to install libraries online
1. Run the verify command to make sure everything is running properly
1. Finally run the upload command

### NOTE: I will upload the wiring diagram as soon
