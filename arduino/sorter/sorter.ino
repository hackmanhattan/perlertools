/* Example sketch to control a 28BYJ-48 stepper motor with ULN2003 driver board and Arduino UNO. More info: https://www.makerguides.com */

// Include the Arduino Stepper.h library:
#include <Servo.h>
#include <Wire.h>
#include "Adafruit_TCS34725.h"
// Define number of steps per rotation:
const int stepsPerRevolution = 512*2;

// Wiring:
// Pin 8 to IN1 on the ULN2003 driver
// Pin 9 to IN2 on the ULN2003 driver
// Pin 10 to IN3 on the ULN2003 driver
// Pin 11 to IN4 on the ULN2003 driver

// Create stepper object called 'myStepper', note the pin order:

char command;
Servo myservo;
Servo funnel_servo;
#define funnel_servo_pin 5
#define servopin 7
#define filter 65
#define home_pos 87
#define graveyard 115
#define move_delay 12
#define wiggle_delay 15
#define wiggle_range 12
#define filter_threshold 4
#define funnel_servo_delay 15
/*
//TCS34725_INTEGRATIONTIME_2_4MS = 0xFF, *< 2.4ms 
TCS34725_INTEGRATIONTIME_24MS =0xF6, /**< 24ms 
TCS34725_INTEGRATIONTIME_50MS = 0xEB, /**< 50ms 
TCS34725_INTEGRATIONTIME_101MS = 0xD5, /**< 101ms 
TCS34725_INTEGRATIONTIME_15w4MS = 0xC0, /**< 154ms 
TCS34725_INTEGRATIONTIME_700MS = 0x00 /**< 700ms 
*/
/*
 * TCS34725_GAIN_1X = 0x00, // No gain 
TCS34725_GAIN_4X = 0x01, // 2x gain 
TCS34725_GAIN_16X = 0x02, //16x gain 
TCS34725_GAIN_60X = 0x03 //60x gain 
 */
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_2_4MS, TCS34725_GAIN_1X);
uint16_t cur_r, cur_g, cur_b;
uint16_t tgt_r, tgt_g, tgt_b;
uint16_t threshold = 3;
int cur_slider_pos = 90;
int cur_funnel_pos = 180;
boolean sort_mode = false;


void setup() {
  // Begin Serial communication at a baud rate of 9600:
  Serial.begin(9600);
  myservo.attach(servopin);
  myservo.write(home_pos);
  funnel_servo.attach(funnel_servo_pin);
  funnel_servo.write(cur_funnel_pos);
  sort_mode=false;
  if (tcs.begin()) {
    Serial.println("R,G,B,Pos");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    //while (1);
  }
  cur_r = 0;
  cur_g = 0;
  cur_b = 0;
}

void loop() {
  read_color(true,2);
  print_color(10);
  if(Serial.available()){
      command = Serial.read();
      if(command=='q') {
        move_slider(cur_slider_pos+1);      
      } else if(command=='e') {
        move_slider(cur_slider_pos-1);
      } else if(command=='i') {
         move_slider(graveyard);
         delay(200);
         move_slider(home_pos);
      } else if(command=='o') {
        middle();
      } else if(command=='p') {
         move_slider(filter);
         delay(200);
         move_slider(home_pos);
      } else if(command=='k') {
          //save color
        save_color(10);
      } else if(command=='l') {
          sort_mode = !sort_mode;
      } else if(command==',') {
          for(int i=0;i<66;i++) {
            middle();
            delay(200);
            move_slider(graveyard);
            delay(200);
          }
      } else if(command=='a') {
        cur_funnel_pos += 20;
        funnel_servo.write(cur_funnel_pos);
        delay(funnel_servo_delay);
      }else if(command=='s') {
        cur_funnel_pos = 90;
        funnel_servo.write(cur_funnel_pos);
        delay(funnel_servo_delay);
      }else if(command=='d') {
        cur_funnel_pos -= 80;
        funnel_servo.write(cur_funnel_pos);
        delay(funnel_servo_delay);
      } else if(command=='g') {
        print_color(10);
      }

  }
  if(sort_mode==true){
    wiggle_funnel();
    middle();
    delay(150);
    read_color(true,10);
    float filter_diff = color_diff(cur_r,cur_g,cur_b,tgt_r,tgt_g,tgt_b);
    Serial.print("filter_diff, ");
    Serial.println(filter_diff);
    if(filter_diff < filter_threshold) {
        Serial.println("filter");
         move_slider(filter);
         delay(200);
         move_slider(home_pos);
    } else {
      Serial.println("graveyard");
         move_slider(graveyard);
         delay(200);
         move_slider(home_pos);
    }
   }
 
}

float color_diff(uint16_t ri,uint16_t gi,uint16_t bi,uint16_t rf,uint16_t gf,uint16_t bf) {
  uint16_t sum = pow((ri-rf),2) + pow((gi-gf),2) + pow((bi-bf),2);
  return sqrt(sum);
}
void middle() {
  myservo.write(home_pos);              // tell servo to go to position in variable 'pos'

    for (int pos = home_pos; pos <home_pos+wiggle_range; pos += 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(wiggle_delay);                       // waits 15ms for the servo to reach the position
      
    }
    for (int pos = home_pos+wiggle_range; pos >home_pos-wiggle_range; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(wiggle_delay);
   
    }
  for (int pos = home_pos-wiggle_range; pos <home_pos; pos += 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(wiggle_delay);                       // waits 15ms for the servo to reach the position
  
  }
  delay(wiggle_delay);                       // waits 15ms for the servo to reach the position
  myservo.write(home_pos);
  cur_slider_pos = home_pos;
}


void move_slider(int tgt_pos) {
  if(tgt_pos > cur_slider_pos) {
   for(int tmp_pos = cur_slider_pos;tmp_pos < tgt_pos;tmp_pos++) {
    myservo.write(tmp_pos); 
   
    delay(move_delay); 
   }
   
  } else {
    for(int tmp_pos = cur_slider_pos;tmp_pos > tgt_pos;tmp_pos--) {
    myservo.write(tmp_pos); 
    delay(move_delay); 
    
   }
  }
  myservo.write(tgt_pos); 
  cur_slider_pos = tgt_pos;
  //Serial.println(cur_slider_pos);
}

void read_color(boolean debug,int read_cnt) {
  uint16_t r,g,b,rt, gt, bt, c, colorTemp, lux;
  rt = gt = bt = 0;
  for(int i=0;i<read_cnt;i++) {
     tcs.getRawData(&r, &g, &b, &c);
     rt += r;
     gt += g;
     bt += b;
  }
  
    cur_r = rt/read_cnt;
    cur_g = gt/read_cnt;
    cur_b = bt/read_cnt;
}

void save_color(int tgt_read_cnt) {
  Serial.println("saving current color");
  middle();
  delay(500);
  uint16_t r, g, b, c;
  uint16_t rt, gt, bt;
  rt = gt = bt = 0;
  for(int i=0;i<tgt_read_cnt;i++) {
    tcs.getRawData(&r, &g, &b, &c);
    rt+=r;
    gt+=g;
    bt+=b;
    delay(100);
  }
  
  tgt_r = rt/tgt_read_cnt;
  tgt_g = gt/tgt_read_cnt;
  tgt_b = bt/tgt_read_cnt;
  Serial.print(tgt_r);Serial.print(",");
  Serial.print(tgt_g);Serial.print(",");
  Serial.println(tgt_b);
 
}
void print_color(int tgt_read_cnt) {
  uint16_t r, g, b, c;
  uint16_t rt, gt, bt;
  rt = gt = bt = 0;
  for(int i=0;i<tgt_read_cnt;i++) {
    tcs.getRawData(&r, &g, &b, &c);
    rt+=r;
    gt+=g;
    bt+=b;
  }
  rt = rt/tgt_read_cnt;
  gt = gt/tgt_read_cnt;
  bt = bt/tgt_read_cnt;
  Serial.print(rt); Serial.print(",");
  Serial.print(gt); Serial.print(",");
  Serial.print(bt);Serial.print(",");
  Serial.println(cur_slider_pos*10);
}
void wiggle_funnel() {
funnel_servo.write(150);
delay(200);
funnel_servo.write(50);
delay(200);
funnel_servo.write(150);
}
