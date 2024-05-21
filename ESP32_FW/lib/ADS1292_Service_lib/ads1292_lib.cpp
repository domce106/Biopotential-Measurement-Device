#include "ads1292_lib.h"

float ads1292InternalVrefVal;
bool ads1292VrefExternal;
uint8_t ads1292ID;

//Initialise SPI communication pins and set working modes
void spiInit()
{
  delay(500);

  pinMode(PIN_START, OUTPUT);
  pinMode(PIN_CS, OUTPUT);
  pinMode(PIN_DRDY, INPUT);
  pinMode(PIN_RESET, OUTPUT);
  pinMode(PIN_MISO, INPUT);
  pinMode(PIN_MOSI, OUTPUT);
  pinMode(PIN_SCLK, OUTPUT);

  //initialize SPI interface with
  // CLOCK -- BitOrder -- DataMode.
  //SPI.beginTransaction(SPISettings(1000, MSBFIRST, SPI_MODE1));
  int clock_div = SPI_CLOCK_DIV32;
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);
  //CPOL = 0, CPHA = 1

  SPI.setDataMode(SPI_MODE1);
  // Selecting 1Mhz clock for SPI
  SPI.setClockDivider(clock_div);
  Serial.print("SPI_CLOCK_DIV = ");
  Serial.println(clock_div);

  Serial.println("SPI initialization complete.");
}

//Initialization commands of ads1292
void ads1292Initialization(const int CSPin, const int pwndPin, const int startPin)
{
  //initialization uses typical startup procedure defined in datasheet.
  //reset pwnd pin
  digitalWrite(CSPin, HIGH);
  digitalWrite(pwndPin, HIGH);
  delayMicroseconds(TCLK * 10);

  delay(1000);

  digitalWrite(pwndPin, LOW);
  delayMicroseconds(TCLK * 10);
  digitalWrite(pwndPin, HIGH);
  delayMicroseconds(TCLK * 18);


  digitalWrite(CSPin, LOW);
  delayMicroseconds(TCLK * 10);
  digitalWrite(CSPin, HIGH);
  delayMicroseconds(TCLK * 10);

  //send SDATAC command to get into register writing mode.
  ads1292SPISendCommands(SDATAC, CSPin);

  ads1292RegWrite(ADS1292_REG_CONFIG1, 0b00000010,CSPin); 		//Set sampling rate to 500 SPS
  ads1292RegRead(ADS1292_REG_CONFIG1, CSPin);
  //ads1292RegWrite(ADS1292_REG_CONFIG2, 0b10100000,CSPin);	//Lead-off comp off, test signal disabled
  ads1292RegWrite(ADS1292_REG_CONFIG2, 0b10100011,CSPin); //Test signal on
  ads1292RegRead(ADS1292_REG_CONFIG2, CSPin);
  ads1292RegWrite(ADS1292_REG_CH1SET, 0b00000001,CSPin);
  ads1292RegWrite(ADS1292_REG_CH2SET, 0b11010001,CSPin);
  ads1292RegRead(ADS1292_REG_CH1SET, CSPin);
  ads1292RegRead(ADS1292_REG_CH2SET, CSPin);

  ads1292RegWrite(ADS1292_REG_LOFFSTAT, ads1292RegRead(ADS1292_REG_LOFFSTAT, CSPin) | 0b01000000, CSPin);
  ads1292RegWrite(ADS1292_REG_RESP2, 0b10000011, CSPin);
  ads1292RegWrite(ADS1292_REG_RESP1, 0b00000010, CSPin);
  ads1292SPISendCommands(OFFSETCAL, PIN_CS);
  delayMicroseconds(20000);

  // reading defined values
  //getting device ID
  ads1292ID = ads1292RegRead(ADS1292_REG_ID, CSPin) & 0b00000011;
  Serial.printf("ADS1292 ID:");
  Serial.println(ads1292ID, BIN);

  // Checking voltage reference
  uint8_t Config2Byte = ads1292RegRead(ADS1292_REG_CONFIG2, CSPin);
  if (((Config2Byte >> 5) & 0x01) == 1)
  {
    if (((Config2Byte >> 4) & 0x01) == 0)
    {
      ads1292InternalVrefVal = 2.42;
    }
    else
    {
      ads1292InternalVrefVal = 4.033;
    }
  }
  Serial.printf("Voltage Reference value: ");
  Serial.print(ads1292InternalVrefVal);
  Serial.println("V");

  //getAllRegValues(regValues);

  // go back into reading data continious mode
  digitalWrite(startPin, HIGH);
  delayMicroseconds(TCLK * 10);
  // ads1292SPISendCommands(START, CSPin);

  ads1292SPISendCommands(RDATAC, CSPin);

  Serial.println("ADS1292 startup complete");

}


//communication commands

void ads1292SPISendCommands(unsigned char command,const int CS)
{
  byte data[1];
  //data[0] = dataIn;
  digitalWrite(CS, LOW);
  delayMicroseconds(TCLK);
  digitalWrite(CS, HIGH);
  delayMicroseconds(TCLK);
  digitalWrite(CS, LOW);
  delayMicroseconds(TCLK);
  SPI.transfer(command);
  delayMicroseconds(TCLK);
  digitalWrite(CS, HIGH);
  delayMicroseconds(TCLK);
}

//register Writing
void ads1292RegWrite (unsigned char READ_WRITE_ADDRESS, unsigned char DATA,const int CSPin)
{
  // combine the register address and the command into one byte:
  byte dataToSend = READ_WRITE_ADDRESS | WREG;
  digitalWrite(CSPin, LOW);
  delayMicroseconds(TCLK);
  digitalWrite(CSPin, HIGH);
  delayMicroseconds(TCLK);
  // take the chip select low to select the device:
  digitalWrite(CSPin, LOW);
  delayMicroseconds(TCLK);
  SPI.transfer(dataToSend); //Send register location
  SPI.transfer(0x00);		//number of register to wr
  SPI.transfer(DATA);		//Send value to record into register
  delayMicroseconds(TCLK);
  // take the chip select high to de-select:
  digitalWrite(CSPin, HIGH);
  if (REGISTER_WRITE_PRINTER == 1)
  {
    Serial.println("------");
    Serial.println("Register write print begin");
    Serial.printf("Register location: ");
    Serial.println(dataToSend, BIN);
    //Serial.println("Number of registers to write: %c", 0x00);
    Serial.printf("Sent value: ");
    Serial.println(DATA, BIN);
    Serial.println("Register write print end");
  }
  delayMicroseconds(TCLK);
}

uint8_t ads1292RegRead (unsigned char READ_WRITE_ADDRESS, const int CSPin)
{
  uint32_t output = 0;
  byte dataToSend = READ_WRITE_ADDRESS | RREG;
  digitalWrite(CSPin, LOW);
  delayMicroseconds(TCLK);
  digitalWrite(CSPin, HIGH);
  delayMicroseconds(TCLK);
  // take the chip select low to select the device:
  digitalWrite(CSPin, LOW);
  delayMicroseconds(TCLK);
  SPI.transfer(dataToSend); //Send register location
  SPI.transfer(0x00);		//number of register to wr
  //delay(2);
  output = SPI.transfer(0x00);  //data from ads1292
  delayMicroseconds(TCLK);
  digitalWrite(CSPin, HIGH);

  if (REGISTER_WRITE_PRINTER == 1)
  {
    Serial.println("------");
    Serial.println("Register read print begin");
    Serial.printf("Register location: ");
    Serial.println(dataToSend, BIN);
    //Serial.println("Number of registers to write: %c", 0x00);
    Serial.printf("Read value: ");
    Serial.println(output, BIN);
    Serial.println("Register read print end");
  }
  delayMicroseconds(TCLK);

  return(output);
}

uint8_t tempDataHold[9] {};
void ads1292CollectData(MeasuredDataToSend& data, int DRDYPin, int CSPin)
{
// int testing {0};
//uint64_t start1 = cpu_hal_get_cycle_count();
  SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE1));
    digitalWrite(CSPin, LOW);
    //delayMicroseconds(TCLK * 4);
    for (int i = 0; i < 9; i++)
      {
        tempDataHold[i] = SPI.transfer(0x00);
// if (digitalRead(DRDYPin) == 0)
// {
//   testing++;
// }
// if (testing != 0 && digitalRead(DRDYPin) == 1)
// {
//   Serial.print("Bit number:");
//   Serial.println(i);
//   testing = 0;
// }
      }
  SPI.endTransaction();

    //digitalWrite(CSPin, HIGH);

    data.statusData[data.FillValue] =   ((uint32_t)tempDataHold[0] << 16) | ((uint32_t)tempDataHold[1] << 8) | (uint32_t)tempDataHold[2];
    data.channel1Data[data.FillValue] = ((uint32_t)tempDataHold[3] << 16) | ((uint32_t)tempDataHold[4] << 8) | (uint32_t)tempDataHold[5];
    data.channel2Data[data.FillValue] = ((uint32_t)tempDataHold[6] << 16) | ((uint32_t)tempDataHold[7] << 8) | (uint32_t)tempDataHold[8];
    data.FillValue++;
//uint64_t end = cpu_hal_get_cycle_count();

// if(end - start1 > 10000)
// {
// Serial.print(end - start1);
// Serial.print("\t");
// Serial.println(data.FillValue);
// }
// if (testing != 0)
// {
//   Serial.println(data.channel1, HEX);
// }
}

int getGain(int channelNumber)
{
  uint8_t gain{0};

  ads1292SPISendCommands(SDATAC, PIN_CS);
  if (channelNumber == 1)
  {
    gain = ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS);
  }
  else if (channelNumber == 2)
  {
    gain = ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS);
  }
  else
  {
    Serial.println("Channel number not valid.");
    return(EXIT_FAILURE);
  }
  ads1292SPISendCommands(RDATAC, PIN_CS);

  gain = (gain >> 4) & ~0b11111000;
  
  int gain_int;
  switch(gain)
  {
    case 0b000:
      gain_int = 6;
      break;
    case 0b001:
      gain_int = 1;
      break;
    case 0b010:
      gain_int = 2;
      break;
    case 0b011:
      gain_int = 3;
      break;
    case 0b100:
      gain_int = 4;
      break;
    case 0b101:
      gain_int = 8;
      break;
    case 0b110:
      gain_int = 12;
      break;
    default:
      return(EXIT_FAILURE);
  }
    return(gain_int);
}

int getChannelStatus()
{
  uint8_t channel1;
  uint8_t channel2;

  ads1292SPISendCommands(SDATAC, PIN_CS);

  channel1 = (ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS) >> 7) & 0b00000001;
  channel2 = (ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS) >> 7) & 0b00000001;

  ads1292SPISendCommands(RDATAC, PIN_CS);

  uint8_t channel_status;

  if (channel1 == 0)
  {
    channel_status = 0b00000001;
  }
  else if (channel1 == 1)
  {
    channel_status = 0b00000000;
  }
  else{return(EXIT_FAILURE);}

  if (channel2 == 0)
  {
    channel_status |= 0b00000010;
  }
  else if (channel2 == 1)
  {
    channel_status |= 0b00000000;
  }
  else{return(EXIT_FAILURE);}

  return(channel_status);
}

int setChannelStatus(uint32_t channelStatus)
{
  uint8_t regval1;
  uint8_t regval2;

  ads1292SPISendCommands(SDATAC, PIN_CS);

  regval1 = ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS);
  regval2 = ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS);

  bool channel1_on = ((channelStatus & 0b01) ? true : false);
  bool channel2_on = ((channelStatus & 0b10) ? true : false);

  setSingleChannelStatus(regval1, channel1_on, 1);
  setSingleChannelStatus(regval2, channel2_on, 2);


  ads1292SPISendCommands(RDATAC, PIN_CS);

  return(0);
}

void setSingleChannelStatus(uint8_t regval, bool channel_on, uint8_t channelNum)
{
  uint8_t regPos;

  switch (channelNum)
  {
  case 1:
    regPos = ADS1292_REG_CH1SET;
    break;
  case 2:
    regPos = ADS1292_REG_CH2SET;
    break;
  default:
    break;
  }

  if (channel_on)
  {
    regval &= ~0b10000000;
    ads1292RegWrite(regPos, regval, PIN_CS);
  }
  else
  {
    regval &= ~0b10001111;
    regval |= 0b10000001;
    ads1292RegWrite(regPos, regval, PIN_CS);
  }
}

int getBitrate()
{
  uint8_t regval;

  ads1292SPISendCommands(SDATAC, PIN_CS);

  regval = (ads1292RegRead(ADS1292_REG_CONFIG1, PIN_CS)) & ~0b11111000;

  ads1292SPISendCommands(RDATAC, PIN_CS);

  int bitrate;
  switch(regval)
  {
    case 0b000:
      bitrate = 125;
      break;
    case 0b001:
      bitrate = 250;
      break;
    case 0b010:
      bitrate = 500;
      break;
    case 0b011:
      bitrate = 1000;
      break;
    case 0b100:
      bitrate = 2000;
      break;
    case 0b101:
      bitrate = 4000;
      break;
    case 0b110:
      bitrate = 8000;
      break;
    default:
      return(EXIT_FAILURE);
  }

  return(bitrate);
    
}

int getWorkStatus()
{
  uint8_t regval;
  bool channel1;
  bool channel2;
  int status;
  bool test_on;
  bool channel_on;

  ads1292SPISendCommands(SDATAC, PIN_CS);

  regval = ads1292RegRead(ADS1292_REG_CONFIG2, PIN_CS) & 0b00000010;

  channel1 = ((ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS) & 0b10000000) == 128 ? false : true);

  channel2 = ((ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS) & 0b10000000) == 128 ? false : true);

  ads1292SPISendCommands(RDATAC, PIN_CS);

  switch (regval)
  {
  case 0:
    test_on = false; 
    break;
  case 2:
    test_on = true; 
    break;

  default:
    return{EXIT_FAILURE};
    break;
  }

  if ((channel1 | channel2) & ~test_on)
  {
    status = 2;  //wroking mode
  }

  else if ((channel1 | channel2) & test_on)
  {
    status = 1; //testing mode
  }

  else
  {
    status = 0; //off mode
  }

  return(status);
}

int setRLD(uint32_t rld)
{
  uint8_t regval{0};

  ads1292SPISendCommands(SDATAC, PIN_CS);

  regval = ads1292RegRead(ADS1292_REG_RLDSENS, PIN_CS);

  if(rld != 0)
  {
    regval |= ((uint8_t)rld);
    regval |= 0b00100000;
    regval &= ~0b11000000; //set fmod/16 chop freq
  }
  else
  {
    regval &= ~0b11111111;
    regval |= 0b01000000;
  }

  ads1292RegWrite(ADS1292_REG_RLDSENS, regval, PIN_CS);
  ads1292SPISendCommands(RDATAC, PIN_CS);
  return(0);
  
}

int setGain(uint32_t gain, uint8_t channel)
{
  uint8_t gainAds{0};

  switch(gain)
  {
    case 6:
      gainAds = 0b00000000;
      break;
    case 1:
      gainAds = 0b00010000;
      break;
    case 2:
      gainAds = 0b00100000;
      break;
    case 3:
      gainAds = 0b00110000;
      break;
    case 4:
      gainAds = 0b01000000;
      break;
    case 8:
      gainAds = 0b01010000;
      break;
    case 12:
      gainAds = 0b01100000;
      break;
    default:
      return(1);
  }

  uint8_t regval;

  ads1292SPISendCommands(SDATAC, PIN_CS);

  if (channel == 1)
  {
    regval = ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS);
    regval &= ~0b01110000;
    regval |= gainAds;
    ads1292RegWrite(ADS1292_REG_CH1SET, regval, PIN_CS);
  }
  else if (channel == 2)
  {
    regval = ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS);
    regval &= ~0b01110000;
    regval |= gainAds;
    ads1292RegWrite(ADS1292_REG_CH2SET, regval, PIN_CS);
  }
  else
  {
    return(1);
  }

  ads1292SPISendCommands(OFFSETCAL, PIN_CS);

  delayMicroseconds(20000);

  ads1292SPISendCommands(RDATAC, PIN_CS);

  return(0);
}

int setBitrate(uint32_t bitrate)
{
  uint8_t bitrateAds;

  switch (bitrate)
  {
  case 125:
    bitrateAds = 0b000;
    break;
  case 250:
    bitrateAds = 0b001;
    break;
  case 500:
    bitrateAds = 0b010;
    break;
  case 1000:
    bitrateAds = 0b011;
    break;
  case 2000:
    bitrateAds = 0b100;
    break;
  case 4000:
    bitrateAds = 0b101;
    break;
  case 8000:
    bitrateAds = 0b110;
    break;
  default:
    return(1);
  }

  uint8_t regval;

  ads1292SPISendCommands(SDATAC, PIN_CS);

  regval = ads1292RegRead(ADS1292_REG_CONFIG1, PIN_CS);
  regval &= ~0b00000111;
  regval |= bitrateAds;
  ads1292RegWrite(ADS1292_REG_CONFIG1, regval, PIN_CS);

  ads1292SPISendCommands(RDATAC, PIN_CS);
  return(0);
}

int setWorkStatus(uint32_t workStatusValue)
{
  uint8_t regval;
  uint8_t sendToRegval;

  switch (workStatusValue)
  {
  case 2:
    sendToRegval = 0b00000000; //working mode
    break;
  case 1:
    sendToRegval = 0b00000011; //testing mode
    break;

  default:
    return{EXIT_FAILURE};
    break;
  }

  ads1292SPISendCommands(SDATAC, PIN_CS);

  regval = ads1292RegRead(ADS1292_REG_CONFIG2, PIN_CS) & ~0b00000011;

  regval =  regval | sendToRegval;

  ads1292RegWrite(ADS1292_REG_CONFIG2, regval, PIN_CS);


  uint8_t regval1;
  uint8_t regval2;

  regval1 = ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS);
  regval2 = ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS);

  setSingleChannelWorkStatus(regval1, workStatusValue, 1);
  setSingleChannelWorkStatus(regval2, workStatusValue, 2);


  ads1292SPISendCommands(RDATAC, PIN_CS);

  return(0);
}


void setSingleChannelWorkStatus(uint8_t regval, uint32_t workStatus, uint8_t channelNum)
{
  uint8_t regPos;

  switch (channelNum)
  {
  case 1:
    regPos = ADS1292_REG_CH1SET;
    break;
  case 2:
    regPos = ADS1292_REG_CH2SET;
    break;
  default:
    break;
  }

  if (workStatus == 1)
  {
    regval &= ~0b10001111;
    regval |= 0b00000101;
    ads1292RegWrite(regPos, regval, PIN_CS);
  }
  else if (workStatus == 2)
  {
    regval &= ~0b10001111;
    ads1292RegWrite(regPos, regval, PIN_CS);
  }
}

void getAllRegValues(RegValues& regValues)
{
  ads1292SPISendCommands(SDATAC, PIN_CS);

  regValues.regID = ads1292RegRead(ADS1292_REG_ID, PIN_CS);
  regValues.regCONFIG1 = ads1292RegRead(ADS1292_REG_CONFIG1, PIN_CS);
  regValues.regCONFIG2 = ads1292RegRead(ADS1292_REG_CONFIG2, PIN_CS);
  regValues.regLOFF = ads1292RegRead(ADS1292_REG_LOFF, PIN_CS);
  regValues.regCH1SET = ads1292RegRead(ADS1292_REG_CH1SET, PIN_CS);
  regValues.regCH2SET = ads1292RegRead(ADS1292_REG_CH2SET, PIN_CS);
  regValues.regRLD_SENS = ads1292RegRead(ADS1292_REG_RLDSENS, PIN_CS);
  regValues.regLOFF_SENS = ads1292RegRead(ADS1292_REG_LOFFSENS, PIN_CS);
  regValues.regLOFF_STAT = ads1292RegRead(ADS1292_REG_LOFFSTAT, PIN_CS);
  regValues.regRESP1 = ads1292RegRead(ADS1292_REG_RESP1, PIN_CS);
  regValues.regRESP2 = ads1292RegRead(ADS1292_REG_RESP2, PIN_CS);
  regValues.regGPIO = ads1292RegRead(ADS1292_REG_GPIO, PIN_CS);

  ads1292SPISendCommands(RDATAC, PIN_CS);

}
