//Tikrina, ar gali prisijungti su esamais wifi duomenimis prie tinklo
//Jei duomenu nera arba prisijungti nepavyksta, ijungiamas AP rezimas
//AP rezimas turi startuoti wifi AP rezimu ir sukurti webserveri
//webserveris turi irasyti ivestus wifi duomenis
//Taip pat webserveris turetu parodyt sarasa galimu wifi tinklu (leisti viena pasirinkti)
//Gauta prisijungimo info is webserverio irasoma i atminti ir naudojama prisijungti
//Isjungiamas wifi AP rezimas ir startuojamas normalus wifi prisijungimas

#include "WiFi_webserver_connector.h"
#include <Preferences.h>
#include "wifi_credentials.h"
#include <WiFiMulti.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include "SPIFFS.h"

AsyncWebServer server(80);

CredentialWebserver::CredentialWebserver()
{
    //AsyncWebServer server(80);

    Serial.println("Setting AP (Access Point)…");

    if(!SPIFFS.begin(true)){
        Serial.println("An Error has occurred while mounting SPIFFS");
        return;
    }
    
    IPAddress local_IP(192, 168, 4, 1);
    // Set your Gateway IP address
    IPAddress gateway(192, 168, 4, 1);

    IPAddress subnet(255, 255, 255, 0);
    // IPAddress primaryDNS(8, 8, 8, 8);   //optional
    // IPAddress secondaryDNS(8, 8, 4, 4); //optional

    // // Configures static IP address
    // if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    //     Serial.println("STA Failed to configure");
    // }
    
    WiFi.mode(WIFI_AP);
    WiFi.softAP("ESP32-Access-Point", "admin12345");

    WiFi.softAPConfig(local_IP, gateway, subnet);
    delay(100);

    // Serial.println("IP address: ");
    // Serial.println(WiFi.localIP());
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);


    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request)
    {
        request->send(SPIFFS, "/index.html");
    });

    server.on("/submit", HTTP_POST, std::bind(&CredentialWebserver::handleSubmit, this, std::placeholders::_1));

    server.begin();
}

CredentialWebserver::~CredentialWebserver()
{

}

void CredentialWebserver::handleSubmit(AsyncWebServerRequest *request)
{
    ssid = request->arg("ssid");
    password = request->arg("password");

    Serial.print("Received SSID: ");
    Serial.println(ssid);
    // Serial.print("Received password: ");
    // Serial.println(password);

    credenetialsReceived = true;

    request->send(200, "text/plain", "Received SSID and password.");
}

String& CredentialWebserver::getSsid()
{
    return ssid;
}

String& CredentialWebserver::getPassword()
{
    return password;
}

bool CredentialWebserver::getCredentialStatus()
{
    return credenetialsReceived;
}