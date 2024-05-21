#ifndef WIFI_CREDENTIALS_H
#define WIFI_CREDENTIALS_H

#include <Preferences.h>
#include <WiFiMulti.h>
#include "WiFi_webserver_connector.h"
#include "WiFi.h"

class WifiCredentials
{
    private:
        int numberOfStoredValues = 0;

        Preferences *preferences;
        WiFiMulti wifiMulti;


        int getStoredLength();
        void readCredentials(WiFiMulti& wifiMulti);
        void scanNetworks();
        bool tryConnecting(WiFiMulti& wifiMulti);

    public:
        WifiCredentials();
        ~WifiCredentials();
        bool checkIfValuesExist();
        void setCredentials(WiFiMulti& wifiMulti, String& ssid, String& password);
        
};

#endif