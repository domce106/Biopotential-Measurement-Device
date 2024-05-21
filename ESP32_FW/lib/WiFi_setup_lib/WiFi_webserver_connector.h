#ifndef WIFI_WEBSERVER_CONNECTOR_H
#define WIFI_WEBSERVER_CONNECTOR_H

#include <Preferences.h>
#include "wifi_credentials.h"
#include <WiFiMulti.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include "SPIFFS.h"

class CredentialWebserver
{
    private:
        String ssid;
        String password;
        bool credenetialsReceived{false};

        void handleSubmit(AsyncWebServerRequest *request);

    public:
        CredentialWebserver();
        ~CredentialWebserver();

        String& getSsid();
        String& getPassword();
        bool getCredentialStatus();

};

extern AsyncWebServer server;



#endif