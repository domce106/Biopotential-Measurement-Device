#ifndef UDP_COM_H_
#define UDP_COM_H_

#include <Arduino.h>
#include "WiFi.h"
#include "SPI.h"
#include "AsyncUDP.h"
#include "ads1292_lib.h"
#include "esp_timer.h"
#include "hal/cpu_hal.h"

#define PORT 7757

#define UDP_PACKET_MEASUREMENT_LENGTH         200
#define UDP_PACKET_MEASUREMENT_INFO_LENGTH    7

#define UPD_TASK_PRIORITY   20


//initialization function
void initUdp();


//send function
void sendUdpArr32(uint32_t* arr32, int length, IPAddress IPsender, int port);


//packet process function
void processPacket(AsyncUDPPacket &packet, int port);

void setWorkParameters(uint32_t* workParams, uint8_t length);
void setRegisterValue(uint32_t* regValue);


//response functions
void responseID(IPAddress IPsender, int port);
void responseStatus(IPAddress IPsender, int port);
void responseStatusPeriod(IPAddress IPsender, int port);
void responseWorkParameters(IPAddress IPsender, int port);

void sendTestData(int port);
void measuredDataSendTask(void *pvParameters);
void sendMeasuredData(uint32_t* data, int lengthData, int channelNum, int port);
void statusSendPeriodically(void *placeholderParameter);


//working conversion functions
uint32_t uint8ToUint32(uint8_t* arr8);
void arr8ToArr32(uint8_t* arr8, uint32_t* arr32, int arr32_len);
void uint32ToArr8(uint32_t val32, uint8_t* arr8);

struct workParameters
{
    uint32_t measuringStatus {};
    uint32_t channelStatus {};
    uint32_t bitrate {};
    uint32_t gain1 {};
    uint32_t gain2 {};
};
void workParameterReadInit();

struct MeasuredDataToSend
{
    int FillValue {};
    uint32_t statusData[UDP_PACKET_MEASUREMENT_INFO_LENGTH + UDP_PACKET_MEASUREMENT_LENGTH] {};
    uint32_t channel1Data[UDP_PACKET_MEASUREMENT_INFO_LENGTH + UDP_PACKET_MEASUREMENT_LENGTH] {};
    uint32_t channel2Data[UDP_PACKET_MEASUREMENT_INFO_LENGTH + UDP_PACKET_MEASUREMENT_LENGTH] {};
};

void IRAM_ATTR isr();

#endif