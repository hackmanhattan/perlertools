#include <Adafruit_AS7341.h>
#include <Stepper.h>
#include <Servo.h>
#include "ColorMath.h"


#define SERVO_PIN A2
#define SERVO_CYCLE 200
bool agg_state = true;
Servo agg_servo;

Adafruit_AS7341 as7341;

#define SENSOR_SIZE 8
uint16_t blank_readings[SENSOR_SIZE] = {1,1,1,1,1,1,1,1};
uint16_t tgt_readings[SENSOR_SIZE] = {6,61,52,72,65,54,46,26}; 
uint16_t max_reading[SENSOR_SIZE] = {0,0,0,0,0,0,0,0};
double max_read = 0;
double avg_read = 0.0;

bool sort_mode = false;
unsigned long myTime = 0;
//joystick

#define VRX_PIN  A0 // Arduino pin connected to VRX pin
#define VRY_PIN  A1 // Arduino pin connected to VRY pin
#define SW_PIN 2
// ezButton button(SW_PIN);
#define SORT_MODE_PIN 4
#define WIGGLE_RANGE 10
#define GRAB_RANGE 30
int x_val = 0; // To store value of the X axis
int y_val = 0; // To store value of the Y axis
#define JOYSTICK_CAL_CNT 20
int button_val = 0; // To store value of the button

#define LED_CURRENT 10
#define ATIME_VAL 99
#define ASTEP_VAL 499


#define ENDSTOP_PIN 3
int endstop_val = 0;
#define _RANGE 10
#define CENTER_POS 90

//stepper
#define STEPS_PER_REV 2038
#define CHAMBER_SPEED 6
#define EXHUAST_SPEED 10
int step_dir=0;
Stepper ch_stepper = Stepper(STEPS_PER_REV, 13,11,12,10); //chamber stepper
Stepper ex_stepper = Stepper(STEPS_PER_REV, 8,6,7,5); //exhaust stepper

#define GAP_TO_EXHAUST 200

bool found_buffer = false;
#define PEAK_BUFFER_SIZE 10
double max_readings[PEAK_BUFFER_SIZE];
uint16_t cur_read_array[PEAK_BUFFER_SIZE][SENSOR_SIZE];
ColorMath cm;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  // Wait for communication with the host computer serial monitor
  while (!Serial) {
    delay(1);
  }
  Serial.println("code Starting");
  if (!as7341.begin()){
    Serial.println("code Could not find AS7341");
    while (1) { delay(10); }
  } 
  //initializer buffer

  Serial.println("code\tBUFFER STUFF");
  for(int i=0;i<PEAK_BUFFER_SIZE;i++) {
    for(int j=0;j<SENSOR_SIZE;j++) {
      cur_read_array[i][j] = 1;
    }
  }
  reset_max_array();
  pinMode(ENDSTOP_PIN,INPUT_PULLUP);
  pinMode(SW_PIN, INPUT_PULLUP);
  pinMode(SORT_MODE_PIN,INPUT_PULLUP);

  // SETUP READER
  as7341.enableLED(true);
  as7341.setATIME(ATIME_VAL);
  as7341.setASTEP(ASTEP_VAL);
  as7341.enableSpectralInterrupt(false);
  as7341.setLEDCurrent(LED_CURRENT);
  as7341.setGain(AS7341_GAIN_1X);
  ch_stepper.setSpeed(CHAMBER_SPEED);
  ex_stepper.setSpeed(EXHUAST_SPEED);

  //Servo initialization
  Serial.println("code\tWHATWHAT");
  agg_servo.attach(SERVO_PIN);
  agg_servo.write(90);
  reset_exhaust();
  step_dir = -10;
  //manual
  Serial.println("code\tstarting intial reads");
  for(int i=0;i<PEAK_BUFFER_SIZE;i++) {
    read_cur_color();
    ch_stepper.step(-1);
  }
  Serial.println("code\tSETUP COMPLETE");
}
void reset_max_array(){
  for(int i=0;i<PEAK_BUFFER_SIZE;i++) {
    max_readings[i]=999-i;
  }
  for(int i=0;i<SENSOR_SIZE;i++) {
    max_reading[i]=1;
  }
  Serial.println("code\treset max array compelted");
}
void reset_exhaust() {
  endstop_val = digitalRead(ENDSTOP_PIN);
  while(endstop_val!=0) {
    ex_stepper.step(1);
    endstop_val = digitalRead(ENDSTOP_PIN);
  }
  Serial.println("code exhaust reset complete");
  delay(100);
}
void set_max_reading(uint16_t tgt_read_a[]) {
  for(int i=0;i<SENSOR_SIZE;i++) {
    if(tgt_read_a[i]<max_reading[i]) {
      return;
    }
  }

  for(int i=0;i<SENSOR_SIZE;i++) {
    max_reading[i]= tgt_read_a[i];
  
  }
}
void print_max_color() {
  Serial.print("maxx");
  for(int i=0;i<SENSOR_SIZE;i++) {
    Serial.print(max_reading[i]);
    Serial.print("\t");
  }
  Serial.println("");
}
void read_cur_color() {
  uint16_t cur_reading[SENSOR_SIZE] ={1,1,1,1,1,1,1,1};
  as7341.readAllChannels();
  cur_reading[0] = as7341.getChannel(AS7341_CHANNEL_415nm_F1);
  cur_reading[1] = as7341.getChannel(AS7341_CHANNEL_445nm_F2);
  cur_reading[2] = as7341.getChannel(AS7341_CHANNEL_480nm_F3);
  cur_reading[3] = as7341.getChannel(AS7341_CHANNEL_515nm_F4);
  cur_reading[4] = as7341.getChannel(AS7341_CHANNEL_555nm_F5);
  cur_reading[5] = as7341.getChannel(AS7341_CHANNEL_590nm_F6);
  cur_reading[6] = as7341.getChannel(AS7341_CHANNEL_630nm_F7);
  cur_reading[7] = as7341.getChannel(AS7341_CHANNEL_680nm_F8);
  for(int i=PEAK_BUFFER_SIZE-1;i>0;i--) {
    max_readings[i] = max_readings[i-1];  //shift max readings
    for(int j=0;j<SENSOR_SIZE;j++) {
      cur_read_array[i][j] = cur_read_array[i-1][j];
    }
  }
  for(int i=0;i<SENSOR_SIZE;i++) {
    cur_read_array[0][i] = cur_reading[i];
    Serial.print(cur_read_array[0][i]);
    Serial.print("\t");
  }
  set_max_reading(cur_reading);
  double cur_max = cm.get_trig_diff(cur_reading,blank_readings);
  max_readings[0]=cur_max;
  Serial.print(max_readings[0]);
    
  double cur_diff = cm.get_cos_dist(tgt_readings,cur_reading);
  Serial.print("\t");
  Serial.print(cur_diff,6);
  double cur_max_diff = cm.get_cos_dist(tgt_readings,max_reading);
  Serial.print("\t");
  Serial.println(cur_max_diff,6);
  // step_dir = map_ch_speed(max_readings[0]);
  print_max_color();
}
bool ended_peak() {
  //do stuff to detect the peak
  for(int i=0;i<PEAK_BUFFER_SIZE-1;i++) {
    if(max_readings[i]>max_readings[i+1]) {
      return false;
    }
  }
  return true;
}
int map_ch_speed(int tgt_reading){
  return map(min(tgt_reading,120),10,120,-30,-2);
}
void save_tgt_color() {
  Serial.println("code 0,0,0,0,0,0,0,0,0,0,0");
  as7341.readAllChannels();
}

void loop() {
  // put your main code here, to run repeatedly:
  x_val = analogRead(VRX_PIN);
  y_val = analogRead(VRY_PIN);
  
  button_val = digitalRead(SW_PIN);
  endstop_val = digitalRead(ENDSTOP_PIN);
  sort_mode = digitalRead(SORT_MODE_PIN);

  ch_stepper.step(step_dir);
  
  //if sort_mode enabled
  read_cur_color();
  if(ended_peak()) {
    double cur_diff = cm.get_cos_dist(tgt_readings,max_reading);
    Serial.print("code\twe found a peak ");
    Serial.println(cur_diff,6);
    if(sort_mode) {
      reset_exhaust();
      if(cur_diff<0.002){
        Serial.print("code\tmatch found ");
        Serial.println(cur_diff,6);
        ex_stepper.step(-STEPS_PER_REV*0.2);
      
      } else {
      }
      ch_stepper.step(-STEPS_PER_REV/4);
      ch_stepper.step(int(STEPS_PER_REV*0.1));
      reset_exhaust();
    }
    reset_max_array();

  }
  myTime+=1;

  if(myTime < SERVO_CYCLE) {
    agg_servo.write(90);
  }
  if(myTime >SERVO_CYCLE && myTime < SERVO_CYCLE+50){
    agg_servo.write(96);
  }
  if(myTime>SERVO_CYCLE+50) {
    myTime = 0;
  }
}
