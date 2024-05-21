#include "udp_com.h"

//UDP communication library

//IPsender_const is not always used, figure out at some point.

int statusSendPeriod{10000};

//SemaphoreHandle_t xMutex;

SemaphoreHandle_t xMutex = xSemaphoreCreateMutex();

uint32_t packetCounter1{0};
uint32_t packetCounter2{0};

bool ipReceived = false;
IPAddress IPsender_const;

//EventGroupHandle_t xEventGroupCreate( void );
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

EventGroupHandle_t xMeasuringEventGroup = xEventGroupCreate();

AsyncUDP udp;
workParameters workParametersData;
RegValues regValuesUDP;

//Inicializes UDP communication.
void initUdp()
{
    workParameterReadInit();
    getAllRegValues(regValuesUDP);

    xTaskCreate(statusSendPeriodically, "Send status periodically", 8192, NULL, UPD_TASK_PRIORITY, NULL);

    if (udp.listen(PORT)) {
    Serial.print("UDP Listening on IP: ");
    Serial.println(WiFi.localIP());

    //When packet is received does the following:
    udp.onPacket([](AsyncUDPPacket packet)
    {
        // Serial.println(xPortGetCoreID());
        // Serial.print("UDP Packet Type: ");
        // Serial.print(packet.isBroadcast() ? "Broadcast" : packet.isMulticast() ? "Multicast" : "Unicast");
        // Serial.print(", From: ");
        // Serial.print(packet.remoteIP());
        // Serial.print(":");
        // Serial.print(packet.remotePort());
        // Serial.print(", To: ");
        // Serial.print(packet.localIP());
        // Serial.print(":");
        // Serial.print(packet.localPort());
        
        processPacket(packet, PORT);
        //processPacket(packet, packet.remotePort()); //testing line with packet sender port
    });
    Serial.println("UDP communication started.");
    Serial.println("Waiting for packet.");
  }
}


//Takes data from packet, parses it and send appropriate answers
void processPacket(AsyncUDPPacket &packet, int port)
{
    //checking if packet correct
    if (packet.length()%4 == 0) 
    {
        ipReceived = true;
        IPsender_const = packet.remoteIP();

        uint length{packet.length()/4};
        uint32_t received_udp [length];
        arr8ToArr32(packet.data(), received_udp, length);

        xSemaphoreTake(xMutex, portMAX_DELAY);
        switch (received_udp[0])
        {
        case 1:
            responseID(packet.remoteIP(), port);
            break;
        case 3:
            responseStatus(packet.remoteIP(), port);
            break;
        case 5:
            statusSendPeriod = received_udp[1];
            responseStatusPeriod(packet.remoteIP(), port);
            break;
        case 7:
            setWorkParameters(received_udp, length);
            responseWorkParameters(packet.remoteIP(), port);
            break;
        case 11:
            setRegisterValue(received_udp);
            responseStatus(packet.remoteIP(), port);
            break;
        default:
            Serial.println("Whoops, we've got an udp package undefined received data problem");
            break;
        }
        xSemaphoreGive(xMutex);
    }
    else
    {
        Serial.println("Whoops, we've got an udp package wrong received data length problem");
    }
  
}

//Converst array from uint8 to uint32 array
void arr8ToArr32(uint8_t* arr8, uint32_t* arr32, int arr32_len)
{
    for (int i = 0; i < arr32_len; i++)
    {
        uint8_t temp[4];
        for (int k = 0; k < 4; k++) {temp[k] = arr8[(i*4)+k];}
        arr32[i] = uint8ToUint32(temp);
    }
}

//Converts uint8 to uint32 singularly
uint32_t uint8ToUint32(uint8_t* arr8)
{
    uint32_t temp = ((uint32_t) arr8[0]<<24) | ((uint32_t) arr8[1]<<16) | ((uint32_t) arr8[2]<<8) | ((uint32_t) arr8[3]);
    return( temp );
}

//Sends response by taking uint32 value array
void sendUdpArr32(uint32_t* arr32, int length, IPAddress IPsender, int port)
{
    int length2 = length*4;
    uint8_t arr8[length2];
    uint8_t temp[4];
    for (int i = 0; i < length; i++)
    {
        uint32ToArr8(arr32[i], temp);
        for (int k = 0; k < 4; k++)
        {
            arr8[i*4 + k] = temp[k];
        }
    }
    //Serial.println("Sending packet");
    udp.writeTo(arr8, length2, IPsender, port);
    //Serial.println("Packet sent");
}

// Converts uint32 to uint8 array
void uint32ToArr8(uint32_t val32, uint8_t* arr8)
{
    arr8[0] = val32 >> 24;
    arr8[1] = val32 >> 16;
    arr8[2] = val32 >> 8;
    arr8[3] = val32;
}

//Sendes responce when received value = 1
void responseID(IPAddress IPsender, int port)
{
    uint8_t length = 4;
    uint32_t arr32[length];
    arr32[0] = 0x02;
    arr32[1] = BOARD_NUMBER;
    arr32[2] = HARDWARE_VERSION;
    arr32[3] = SOFTWARE_VERSION;
    sendUdpArr32(arr32, length, IPsender, port);
}

void responseStatus(IPAddress IPsender, int port)
{
    uint8_t length = 19;
    uint32_t arr32[length];
    arr32[0] = 0x04;                                //begining of answer to status 
    arr32[1] = BOARD_NUMBER;                        //board number
    arr32[2] = workParametersData.measuringStatus;  //work status
    arr32[3] = workParametersData.channelStatus;    //channel status
    arr32[4] = workParametersData.bitrate;          //bitrate 
    arr32[5] = workParametersData.gain1;            //gain1 
    arr32[6] = workParametersData.gain2;            //gain2
    
    arr32[7] = regValuesUDP.regID;
    arr32[8] = regValuesUDP.regCONFIG1;
    arr32[9] = regValuesUDP.regCONFIG2;
    arr32[10] = regValuesUDP.regLOFF;
    arr32[11] = regValuesUDP.regCH1SET;
    arr32[12] = regValuesUDP.regCH2SET;
    arr32[13] = regValuesUDP.regRLD_SENS;
    arr32[14] = regValuesUDP.regLOFF_SENS;
    arr32[15] = regValuesUDP.regLOFF_STAT;
    arr32[16] = regValuesUDP.regRESP1;
    arr32[17] = regValuesUDP.regRESP2;
    arr32[18] = regValuesUDP.regGPIO;

    
    sendUdpArr32(arr32, length, IPsender, port);
}

void responseStatusPeriod(IPAddress IPsender, int port)
{
    uint8_t length = 3;
    uint32_t arr32[length];

    arr32[0] = 0x06; //begining of answer to status period
    arr32[1] = BOARD_NUMBER; //board number
    arr32[2] = 0x00; //placeholder for error

    sendUdpArr32(arr32, length, IPsender, port);
}

void responseWorkParameters(IPAddress IPsender, int port)
{
    uint8_t length = 3;
    uint32_t arr32[length];

    arr32[0] = 0x08; //begining of answer to work parameters
    arr32[1] = BOARD_NUMBER; //board number
    arr32[2] = 0x00; //placeholder for error

    sendUdpArr32(arr32, length, IPsender, port);
}

void sendTestData(int port)
{
    //check if there is a saved IP from a received udp package
    if (ipReceived == true & workParametersData.measuringStatus != 0)
    {
        uint8_t length = UDP_PACKET_MEASUREMENT_LENGTH + UDP_PACKET_MEASUREMENT_INFO_LENGTH;
        uint8_t measurement_length = UDP_PACKET_MEASUREMENT_LENGTH;
        uint32_t arr32[length];

        arr32[0] = 0x0A; //begining of sending measured data
        arr32[1] = BOARD_NUMBER; //board number
        arr32[2] = 0x01; //channel number placeholder
        arr32[3] = workParametersData.bitrate; //bitrate
        arr32[4] = workParametersData.gain1; //gain1
        arr32[5] = packetCounter1; //counts number of packets sent
        packetCounter1++;
        arr32[6] = measurement_length; //number of measurements

        for(int i = 1; i<=measurement_length; i++)
        {
            arr32[i+6] = i;
        }

        sendUdpArr32(arr32, length, IPsender_const, port);
    }
}

void statusSendPeriodically(void *placeholderParameter)
{
    Serial.println("Task size send periodically:");
    Serial.println(uxTaskGetStackHighWaterMark(NULL));
    for(;;)
    {
        vTaskDelay(statusSendPeriod);
        if (ipReceived == true)
        {
            xSemaphoreTake(xMutex, portMAX_DELAY);
            responseStatus(IPsender_const, PORT);
            xSemaphoreGive(xMutex);
        }
    }
}


void setWorkParameters(uint32_t* workParams, uint8_t length)
{
    int checkError{0};

    if (workParams[1] == 0)
    {
        ads1292SPISendCommands(SDATAC, PIN_CS);
        workParametersData.measuringStatus = 0;
        xEventGroupClearBits(xMeasuringEventGroup, 1<<1);
    }
    else
    {
        checkError += setWorkStatus(workParams[1]);
        workParametersData.measuringStatus = getWorkStatus();
        xEventGroupSetBits(xMeasuringEventGroup, 1<<1);
    }
    checkError += setChannelStatus(workParams[2]);
    workParametersData.channelStatus = getChannelStatus();

    checkError += setBitrate(workParams[3]);
    workParametersData.bitrate = getBitrate();

    checkError += setGain(workParams[4], 1);
    workParametersData.gain1 = getGain(1);

    checkError += setGain(workParams[5], 2);
    workParametersData.gain2 = getGain(2);

    checkError += setRLD(workParams[6]);

    getAllRegValues(regValuesUDP);


    if (checkError != 0)
    {
        Serial.println("ERROR");
    }
}

void setRegisterValue(uint32_t* regValue)
{
    ads1292SPISendCommands(SDATAC, PIN_CS);

    ads1292RegWrite(static_cast<uint8_t>(regValue[1]), static_cast<uint8_t>(regValue[2]), PIN_CS);

    ads1292SPISendCommands(OFFSETCAL, PIN_CS);

    delayMicroseconds(20000);

    ads1292SPISendCommands(RDATAC, PIN_CS);
    
    getAllRegValues(regValuesUDP);
}

void workParameterReadInit()
{
    workParametersData.measuringStatus = 0;
    xEventGroupClearBits(xMeasuringEventGroup, 1<<1);
    workParametersData.channelStatus = getChannelStatus();
    workParametersData.bitrate = getBitrate();
    workParametersData.gain1 = getGain(1);
    workParametersData.gain2 = getGain(2);
}


void IRAM_ATTR isr() {
    xEventGroupSetBitsFromISR(xMeasuringEventGroup, 1, &xHigherPriorityTaskWoken);
}


void measuredDataSendTask(void *pvParameters)
{
    MeasuredDataToSend measuredData {};
    measuredData.FillValue = UDP_PACKET_MEASUREMENT_INFO_LENGTH;

    Serial.println("Task size:");
    Serial.println(uxTaskGetStackHighWaterMark(NULL));

    for(;;)
    {
            xEventGroupWaitBits(xMeasuringEventGroup, 0b11, pdFALSE, pdTRUE, portMAX_DELAY);
            uint64_t start = esp_timer_get_time();
            //uint64_t start = cpu_hal_get_cycle_count();
            xSemaphoreTake(xMutex, portMAX_DELAY);
            ads1292CollectData(measuredData, PIN_DRDY, PIN_CS);

            if (measuredData.FillValue == UDP_PACKET_MEASUREMENT_INFO_LENGTH + UDP_PACKET_MEASUREMENT_LENGTH)
            {
                //Serial.println("HERE");
                if (workParametersData.channelStatus == 1 || workParametersData.channelStatus == 3)
                {
                    sendMeasuredData(measuredData.channel1Data, UDP_PACKET_MEASUREMENT_INFO_LENGTH + UDP_PACKET_MEASUREMENT_LENGTH, 1, PORT);
                }
                if (workParametersData.channelStatus == 2 || workParametersData.channelStatus == 3)
                {
                    sendMeasuredData(measuredData.channel2Data, UDP_PACKET_MEASUREMENT_INFO_LENGTH + UDP_PACKET_MEASUREMENT_LENGTH, 2, PORT);
                }
                measuredData.FillValue = UDP_PACKET_MEASUREMENT_INFO_LENGTH;
            }
            xSemaphoreGive(xMutex);
            uint64_t end = esp_timer_get_time();
            //uint64_t end = cpu_hal_get_cycle_count();
            if (end - start > 125)
            {
                //Serial.println(end - start);
            }
            //Serial.println(end - start);
            xEventGroupClearBits(xMeasuringEventGroup, 1);
        
    }

}

void sendMeasuredData(uint32_t* data, int length, int channelNum, int port)
{

    data[0] = 0x0A; //begining of sending measured data
    data[1] = BOARD_NUMBER; //board number
    data[2] = channelNum; //channel number
    data[3] = workParametersData.bitrate; //bitrate
    if (channelNum == 1)
    {
        data[4] = workParametersData.gain1; //gain1
        data[5] = packetCounter1; //counts number of packets sent
        packetCounter1++;
    }
    else
    {
        data[4] = workParametersData.gain2; //gain2
        data[5] = packetCounter2; //counts number of packets sent
        packetCounter2++;
    }
    
    data[6] = length - UDP_PACKET_MEASUREMENT_INFO_LENGTH; //number of measurements

    sendUdpArr32(data, length, IPsender_const, port);
}



