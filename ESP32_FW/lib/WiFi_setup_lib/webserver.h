#ifndef WEBSERVER_H_
#define WEBSERVER_H_

#include "WiFi.h"

void wifiConnect(const char* ssid, const char* pass);
void wifiIP();

#endif