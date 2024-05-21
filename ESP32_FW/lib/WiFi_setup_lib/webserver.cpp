#include "webserver.h"

void wifiConnect(const char* ssid, const char* pass)
{
    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, pass);
    while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    }
    Serial.println("------");
    Serial.print("Connected to wifi: ");
    Serial.println(WiFi.SSID());
    Serial.println("------");
    Serial.print("On IP: ");
    Serial.println(WiFi.localIP());
}

void wifiIP()
{
    Serial.println(WiFi.localIP());
}