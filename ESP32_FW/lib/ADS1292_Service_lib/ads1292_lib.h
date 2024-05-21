
#ifndef ADS1292_LIB_H_
#define ADS1292_LIB_H_

#include "udp_com.h"
#include <Arduino.h>
#include <SPI.h>
#include "hal/cpu_hal.h"

//Versions
#define HARDWARE_VERSION  0x0100
#define SOFTWARE_VERSION  0x0100
#define BOARD_NUMBER      0X01


//SPI pin definitions
#define PIN_START   22
#define PIN_DRDY    17
#define PIN_CS      5 //default SS pin is 5
#define PIN_MISO    19 // default pin is 19
#define PIN_MOSI    23  // default is 23
#define PIN_SCLK    18 // default is 18
#define PIN_RESET   21

#define REGISTER_WRITE_PRINTER  1  //if 1, prints written registers.
#define REGISTER_READ_PRINTER   1  //if 1, prints read registers.

// Register Read Commands
#define RREG    0x20		//Read n nnnn registers starting at address r rrrr
                      //first byte 001r rrrr (2xh)(2) - second byte 000n nnnn(2)
#define WREG    0x40	  //Write n nnnn registers starting at address r rrrr
                      //first byte 010r rrrr (2xh)(2) - second byte 000n nnnn(2)
#define START	  0x08		//Start/restart (synchronize) conversions
#define STOP	  0x0A		//Stop conversion
#define RDATAC  0x10		//Enable Read Data Continuous mode.

#define OFFSETCAL   0x1A

//This mode is the default mode at power-up.
#define SDATAC    0x11		//Stop Read Data Continuously mode
#define RDATA	    0x12		//Read data by command; supports multiple read back.

#define SPI_DUMMY_DATA  0xFF //Dummy data to send when capturing data.

//register address
#define ADS1292_REG_ID			  0x00
#define ADS1292_REG_CONFIG1		0x01
#define ADS1292_REG_CONFIG2		0x02
#define ADS1292_REG_LOFF		  0x03
#define ADS1292_REG_CH1SET		0x04
#define ADS1292_REG_CH2SET		0x05
#define ADS1292_REG_RLDSENS		0x06
#define ADS1292_REG_LOFFSENS  0x07
#define ADS1292_REG_LOFFSTAT  0x08
#define ADS1292_REG_RESP1	    0x09
#define ADS1292_REG_RESP2	    0x0A
#define ADS1292_REG_GPIO	    0x0B

#define TCLK  10 // 4*t_clk when f_clk = 512kHz


// defining global variables
extern uint8_t ads1292ID;
extern float ads1292InternalVrefVal;
extern bool ads1292VrefExternal;
extern const float ads1292BitDivisor;

void spiInit();
void ads1292Initialization(const int CSPin, const int pwndPin, const int startPin);

void ads1292SPISendCommands(unsigned char command,const int CS);
void ads1292RegWrite (unsigned char READ_WRITE_ADDRESS, unsigned char DATA,const int chipSelect);
uint8_t ads1292RegRead (unsigned char READ_WRITE_ADDRESS, const int CSPin);

struct MeasuredDataToSend;
void ads1292CollectData(MeasuredDataToSend& data, int DRDYPin, int CSPin);

int getGain(int channelNumber);
int getChannelStatus();
int getBitrate();
int getWorkStatus();

int setRLD(uint32_t rld);

int setGain(uint32_t gain, uint8_t channel);
int setBitrate(uint32_t bitrate);
int setChannelStatus(uint32_t channelStatus);
void setSingleChannelStatus(uint8_t regval, bool channel_on, uint8_t channelNum);
int setWorkStatus(uint32_t workStatusValue);
void setSingleChannelWorkStatus(uint8_t regval, uint32_t workStatus, uint8_t channelNum);
struct RegValues
{
    uint32_t regID;
    uint32_t regCONFIG1;
    uint32_t regCONFIG2;
    uint32_t regLOFF;
    uint32_t regCH1SET;
    uint32_t regCH2SET;
    uint32_t regRLD_SENS;
    uint32_t regLOFF_SENS;
    uint32_t regLOFF_STAT;
    uint32_t regRESP1;
    uint32_t regRESP2;
    uint32_t regGPIO;
};

void getAllRegValues(RegValues& regValues);


#endif
