//#include <AFMotor.h>
//#include <OneWire.h>
//#include <DallasTemperature.h>
#include <Servo.h>
#include <Q2HX711.h>
#define HEADER 0xA0
#define FOOTER 0x0B
#define TDS_PIN A0
#define TEMP_PIN 2
#define PH_PIN A3
#define MASS_PIN 3
#define MASS_CLOCK 4
#define PH_OFFSET 0
#define SENS_DELAY 1000
#define WEIGHT_X1 9243475
#define WEIGHT_X0 8951688
#define WEIGHT_Y1 600
#define SERVO_PIN 7

volatile Servo foodServo;

uint8_t command;
uint8_t data[256];
uint8_t dataLen = 0;
int currDataIndex = 0;
bool headerFound = false;

//OneWire oneWire(TEMP_PIN);
//DallasTemperature sensor(&oneWire);

float temp = 25;
float pH = 7;
float tds = 100;
float foodWeight = 10;

Q2HX711 hx711(MASS_PIN, MASS_CLOCK);
unsigned long deltaTime;
unsigned long pastTime;
long sensClock = 0;

volatile int feedQueued = 0;
volatile int timerDelay = 0;  // attempt to create 
volatile bool feedPosition = true; // true: facing up, false: facing down

void setup() {
  // put your setup code here, to run once:
  cli();  // cli stops global interrupt
//  sensor.begin();
  Serial.begin(9600);
  pinMode(PH_PIN, INPUT);
  pinMode(TDS_PIN, INPUT);
  foodServo.attach(SERVO_PIN);
  foodServo.write(0); // should start facing up
  pastTime = 0;

  //(see atmel 328/168)
  // set up interupts
  // timer 0: 1Hz (after software additional register)
  // timer register flags
  TCCR0A = 0; 
  TCCR0B = 0;

  TCNT0 = 0;  // timer register (8 bit)
  OCR0A = 125;  // timer compare registers (compared with TCNT1)
  // sets flags in register a so 
  TCCR0A |= (1 << WGM01); // enable CTC
  TCCR0B |= (1 << CS02) | (1 << CS00);  // sets clock prescaler timing
  TIMSK0 |= (1 << OCIE0A);  // compare interupt enabled

  sei();  // sei starts global interrupt
}

void loop() {
  unsigned long now = millis();
  deltaTime = now - pastTime;
  pastTime = now;
  if (sensClock < 0){
    readSensors();
    sensClock = SENS_DELAY;
  }
  else{
    sensClock -= deltaTime;
  }
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
          dataLen = 4;
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
          case 0x1A:  // add to feed num
            feedQueued += ((int*)data)[0];
          break;
        }
      }
      resetWriteData();
    }
  }
}

void resetWriteData(){
  currDataIndex = 0;
  for (int i = 0; i < 255; i++){
    data[i] = 0;
  }
  headerFound = false;
  dataLen = 0;
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
  long reading = hx711.read();
  float ratio_1 = (float) (reading-WEIGHT_X0);
  float ratio_2 = (float) (WEIGHT_X1-WEIGHT_X0);
  float ratio = ratio_1/ratio_2;
  float foodWeight = WEIGHT_Y1*ratio;
  
  // pH sensor
  float pHVol = analogRead(PH_PIN)*5.0/1024;  // why isn't this 5?
  pH = pHVol*3.5+PH_OFFSET;

  // temp sensor
//  sensor.requestTemperatures();
//  temp = sensor.getTempCByIndex(0);


  // tds sensor
  float tdsCo = 1.0+0.02*(temp-25.0);
  float tdsVol = (analogRead(TDS_PIN) * 5 / 1024) / tdsCo;
  tds = (133.42*tdsVol*tdsVol*tdsVol - 255.86*tdsVol*tdsVol + 857.39*tdsVol)*0.5;

//  Serial.print("---");
//  Serial.print("weight: ");
//  Serial.println(foodWeight);
//  Serial.print("pH: ");
//  Serial.println(pH);
//  Serial.print("temp: ");
//  Serial.println(temp);
//  Serial.print("tds: ");
//  Serial.println(tds);
  sendData(0x01, foodWeight);
  sendData(0x02, pH);
//  sendData(0x03, temp);
  sendData(0x03, tds);
}

void calcMovingAverage(){

}

ISR(TIMER0_COMPA_vect){ // timer 1 occured! Manage feeding servo
  if (timerDelay >= 125){  //timer delay is an additional software timer so the hz is lower. Target is 1hz.
    if (feedPosition && (feedQueued > 0)){
      feedQueued--;
      feedPosition = false;
      foodServo.write(180);
    }
    else{
      foodServo.write(0);
      feedPosition = true;
    }
    timerDelay = 0;
  }
  else{
    timerDelay++;
  }
}
