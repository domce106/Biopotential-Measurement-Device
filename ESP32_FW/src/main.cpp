#include <Arduino.h>
//#include <SPI.h>
#include "udp_com.h"
#include "ads1292_lib.h"
#include "webserver.h"
#include "wifi_credentials.h"
#include "WiFi_webserver_connector.h"

//TODO galios spektras kompe
//TODO waterfall spekttras kompe
//TODO Jei negaunama uzklausa is kompo ilgai, tai sustabdomas veikimas
//TODO Viska perrasyt su klasem, kad butu patogiau.
//TODO prideti RLD esp32 ir desktop. Ijungti isjungti funkcija
//TODO Kartais SPI letai nuskaito duomenis
//TODO klaidu issiuntimas atsakymuose
//TODO sudeti funkcijas i labiau tinkancius failus
//TODO padaryti klases, kuriomis operuojant galima butu naudotis keliais ads1292
//TODO geriau dokumentuoti koda
  //TODO .h failuose aprasyti ka priimima ir ka grazina, bei ttrumpai ka daro
  //TODO .cpp failuose tiksliau aprasyti kaip viskas veikia

const char* ssid = "ssid";
const char* pass = "password";

void setup() {
  Serial.begin(115200);
  Serial.print("yes");
  spiInit();  //initalize spi
  ads1292Initialization(PIN_CS, PIN_RESET, PIN_START);  //initialize ads1292

  //WifiCredentials wifiCredentials;

  wifiConnect(ssid, pass);

  initUdp();

  xTaskCreate(measuredDataSendTask, "Send Data Task", 8192, NULL, UPD_TASK_PRIORITY, NULL);

  attachInterrupt(PIN_DRDY, isr, FALLING);

  //Serial.println(getCpuFrequencyMhz());

}

void loop() {
  //SPI_Data = ads1292DataCollectAndParse(PIN_DRDY, PIN_CS);
  //Serial.println(SPI_Data.ecg, 8);
  //delay(10000);
  //sendMeasuredData(PORT);
}