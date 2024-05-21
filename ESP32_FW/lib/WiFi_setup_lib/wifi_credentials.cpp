#include <Preferences.h>
#include "wifi_credentials.h"
#include <WiFiMulti.h>
#include "WiFi_webserver_connector.h"
#include "WiFi.h"

//Atidaromas failas ir nuskaitomi duomenys
//Jei duomenu nera -- isijungia duomenu gavimo metodai (ESP32 webserveris)
//Jei duomenys yra, tai paimimami wifi credentials ir bandoma prisijungti prie tinklo. Pirma imamam ssid ir ziurima, ar yra toks tinkle.

//Nuskaitomi matomi SSID ir ju stipriai.
//Nuskaitomi issaugoti SSID
//Jei yra sutampanciu, tai prijungiama pagal stipri
//Jei nera sutampanciu, leidziama irasymo programa is wifi_webserver_connector

//Kai ivedami nauji duomenys, reikia juos irasyti. Pageidautina encryptintus.

WifiCredentials::WifiCredentials()
{
    preferences = new Preferences();
    preferences->begin("credentials", false);
    numberOfStoredValues = getStoredLength();
    //There are values saved in memory
    if(numberOfStoredValues != 0)
    {
        readCredentials(wifiMulti);
        //Failed to connect
        if (tryConnecting(wifiMulti) != true)
        {
            CredentialWebserver credentialWebserver;
            while (credentialWebserver.getCredentialStatus() != true)
            {
                if (credentialWebserver.getCredentialStatus() == true)
                {
                    setCredentials(wifiMulti, credentialWebserver.getSsid(), credentialWebserver.getPassword());
                }
            }
        }
        tryConnecting(wifiMulti);
    }
    //No values saved in memory
    else
    {
        CredentialWebserver credentialWebserver;
        while (credentialWebserver.getCredentialStatus() != true)
        {
            if (credentialWebserver.getCredentialStatus() == true)
            {
                setCredentials(wifiMulti, credentialWebserver.getSsid(), credentialWebserver.getPassword());
            }
        }
        tryConnecting(wifiMulti);
    }
    
}

WifiCredentials::~WifiCredentials()
{
    delete preferences;
}

int WifiCredentials::getStoredLength()
{
    int len = preferences->getInt("len", 0);
    return len;
}

bool WifiCredentials::checkIfValuesExist()
{
    if (numberOfStoredValues != 0)
    {
        return true;
    }
    return false;
}

void WifiCredentials::readCredentials(WiFiMulti& wifiMulti)
{
    for (int i = 0; i < numberOfStoredValues; i++)
    {
        wifiMulti.addAP(
            preferences->getString("ssid" + numberOfStoredValues, "").c_str(),
            preferences->getString("password" + numberOfStoredValues, "").c_str()
        );
    }
}

void WifiCredentials::setCredentials(WiFiMulti& wifiMulti, String& ssid, String& password)
{
    preferences->putString("ssid" + numberOfStoredValues, ssid);
    preferences->putString("password" + numberOfStoredValues, password);
    preferences->putInt("len", numberOfStoredValues++);

    wifiMulti.addAP(ssid.c_str(), password.c_str());
}

bool WifiCredentials::tryConnecting(WiFiMulti& wifiMulti)
{
    unsigned long startMeasure { millis() };
    unsigned long maxWaitTime { startMeasure + 5000};
    WiFi.mode(WIFI_STA);
    Serial.println("Connecting Wifi...");
    while (wifiMulti.run() != WL_CONNECTED)
    {
        if (millis()- startMeasure >= maxWaitTime) 
        {
        Serial.println("Network Failed");
        WiFi.mode(WIFI_OFF);
        delay(100);
        return(false);
        }
    }
    return(true);
}

void WifiCredentials::scanNetworks()
{
    WiFi.mode(WIFI_STA);
    int n = WiFi.scanNetworks();
    WiFi.mode(WIFI_OFF);
}
