#include <AFMotor.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define HEADER 0xA0
#define FOOTER 0x0B
#define TDS_PIN A0
#define TEMP_PIN 2
#define PH_PIN A3
#define MASS_PIN 3
#define MASS_CLOCK 4
#define PH_OFFSET 0

AF_DCHotor motor(3);

uint8_t command;
uint8_t data[256];
uint8_t dataLen = 0;
int currDataIndex = 0;
bool headerFound = false;

OneWire oneWire(TEMP_PIN);
DallasTemperature sensor(&oneWire);

float temp = 25;
float pH = 7;
float tds = 100;
float foodWeight = 10;

Q2H711 hx711(MASS_PIN, MASS_CLOCK);

void setup() {
  // put your setup code here, to run once:
  sensor.begin();
  Serial.begin(112500);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    uint8_t val = Serial.read();
    // check for header
    if (!headerFound){
      if (val == HEADER){
        headerFound = true;
        currDataIndex++;
      }
    }
    // get the command byte and expected length of data
    else if (currDataIndex == 1){
      command = val;
      // get length of data to read
      switch (command){
        case 0x1A:
          dataLen = 24;
          deviceSel = 0x00;
        break;
        case 0x1B:
          dataLen = 24;
          deviceSel = 0x00;
        break;
        default:
          resetWriteData();
        break;
      }
      currDataIndex++;
    }
    // read the data
    else if ((currDataIndex-2) < dataLen){
      data[currDataIndex-2] = val;
      currDataIndex++;
    }
    else{ // check footer
      if (val == FOOTER){
        switch (command){
          case 0x1A:
          break;
          case 0x1B:
          break;
        }
      }
      resetWriteData();
    }
  }
}

void sendData(byte indicator, float data){
  Serial.write(HEADER);
  Serial.write(indicator);
  for (int i = 0; i < 4; i++){
    Serial.write(((byte*)&data)[i]);
  }
  Serial.write(FOOTER);
}

void readSensors(){
  // weight sensor
  foodWeight = hx711.read()/100.0;

  // pH sensor
  float pHVol = analogRead(PH_PIN)*5/1024;  // why isn't this 5?
  pH = pHVol*3.5+PH_OFFSET;

  // temp sensor
  sensor.requestTemperatures();
  temp = sensor.getTempCByIndex(0);

  // tds sensor
  float tdsCo = 1.0+0.02*(temperature-25.0);
  float tdsVol = (analogRead(TDS_PIN) * 5 / 1024) / tdsCo;
  tds = (133.42*tdsVol*tdsVol*tdsVol - 255.86*tdsVol*dsVol + 857.39*tdsVol)*0.5;

  sendData(0x01, foodWeight);
  sendData(0x02, pH);
  sendData(0x03, temp);
  sendData(0x04, tds);

}

void calcMovingAverage(){

}

void resetWriteData(){
  currDataIndex = 0;
  for (int i = 0; i < 255; i++){
    data[i] = 0;
  }
  headerFound = false;
  dataLen = 0;
}