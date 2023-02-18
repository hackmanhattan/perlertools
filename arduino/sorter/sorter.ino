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
Servo slider_servo;
Servo funnel_servo;
#define funnel_servo_pin 5
#define slider_servo_pin 7
#define filter_pos 55
#define home_pos 95
#define graveyard_pos 130
#define move_delay 12
#define wiggle_delay 100
#define wiggle_range 15

#define funnel_servo_delay 15
#define funnel_home 90
#define scan_delay 40
#define middle_delay 10
#define filter_threshold 150
/*
//TCS34725_INTEGRATIONTIME_2_4MS = 0xFF, *< 2.4ms 
TCS34725_INTEGRATIONTIME_24MS =0xF6, /**< 24ms 
TCS34725_INTEGRATIONTIME_50MS = 0xEB, /**< 50ms 
TCS34725_INTEGRATIONTIME_101MS = 0xD5, /**< 101ms 
TCS34725_INTEGRATIONTIME_154MS = 0xC0, /**< 154ms 
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

uint16_t threshold = 50;
int cur_slider_pos = 90;
int cur_funnel_pos = 90;
boolean sort_mode = false;
unsigned long last_millis = 0;

void setup() {
  // Begin Serial communication at a baud rate of 9600:
  Serial.begin(9600);
  slider_servo.attach(slider_servo_pin);
  slider_servo.write(home_pos);
  funnel_servo.attach(funnel_servo_pin);
  funnel_servo.write(cur_funnel_pos);
  sort_mode=false;
     Serial.println("R,G,B,Pos");
  if (tcs.begin()) {
 
  } else {
//    Serial.println("No TCS34725 found ... check your connections");
    //while (1);
  }
  tgt_r = tgt_g = tgt_b = 1024;
  cur_r = 0;
  cur_g = 0;
  cur_b = 0;
}

void loop() {

  if(Serial.available()){
      command = Serial.read();
      if(command=='q') {
        move_slider(cur_slider_pos+1);      
      } else if(command=='e') {
        move_slider(cur_slider_pos-1);
      } else if(command=='w') {
        scan_color(false);
      } else if(command=='i') {
         move_slider(graveyard_pos);
         delay(200);
       
      } else if(command=='o') {
        middle();
      } else if(command=='p') {
         move_slider(filter_pos);
         delay(200);
   
      } else if(command=='k') {
          //save color
        save_color(true);
      } else if(command=='l') {
          //prime the chamber
          if(sort_mode) {
            funnel_servo.write(funnel_home);
          } else {
            funnel_servo.write(funnel_home-6);
          }
          sort_mode = !sort_mode;
      } else if(command==',') {
          for(int i=0;i<66;i++) {
            middle();
            delay(200);
            move_slider(graveyard_pos);
            delay(200);
          }
      } else if(command=='a') {
        cur_funnel_pos += 2;
        funnel_servo.write(cur_funnel_pos);
        delay(funnel_servo_delay);
      }else if(command=='s') {
        cur_funnel_pos = 90;
        funnel_servo.write(cur_funnel_pos);
        delay(funnel_servo_delay);
      }else if(command=='d') {
        cur_funnel_pos -= 2;
        funnel_servo.write(cur_funnel_pos);
        delay(funnel_servo_delay);
      } else if(command=='g') {
        print_color(10);
      }

  }
  if(sort_mode==true){
    middle();
    delay(150);
    scan_color(true);
    float filter_diff = color_diff(cur_r,cur_g,cur_b,tgt_r,tgt_g,tgt_b);
    Serial.print("cur_r:");Serial.print(cur_r);
    Serial.print(" cur_g:");Serial.print(cur_g);
    Serial.print(" cur_b:");Serial.print(cur_b);
    Serial.print(" tgt_r:");Serial.print(tgt_r);
    Serial.print(" tgt_g:");Serial.print(tgt_g);
    Serial.print(" tgt_b:");Serial.print(tgt_b);
    Serial.print(" filter:");Serial.println(filter_diff);
    if(filter_diff < filter_threshold) {
        Serial.println("filter");
         move_slider(filter_pos);
         delay(200);
         move_slider(home_pos);
    } else {
      Serial.println("graveyard");
         move_slider(graveyard_pos);
         delay(200);
         move_slider(home_pos);
    }
   } else {
      read_color(true);
   }
 
}

double color_diff(long ri,long gi,long bi,long rf,long gf,long bf) {
  long sum = sq(abs(ri-rf)) + sq(abs(gi-gf)) + sq(abs(bi-bf));
  long r_sq = (ri-rf)*(ri-rf);
  Serial.println("color diff:");
  Serial.print(ri);Serial.print("\t");Serial.print(gi);Serial.print("\t");Serial.print(bi);Serial.println("\t");
  Serial.print(rf);Serial.print("\t");Serial.print(gf);Serial.print("\t");Serial.print(bf);Serial.println("\t");
  Serial.print(rf-ri);Serial.print("\t");Serial.print(gf-gi);Serial.print("\t");Serial.print(bf-bi);Serial.println("\t");
  Serial.print(r_sq);Serial.print("~");Serial.print(sq(ri-rf));
  
  Serial.println("");
  return sqrt(sum);
}
void middle() {
  // ease to middle
  Serial.print("cur slider pos: ");Serial.println(cur_slider_pos);
  if(cur_slider_pos < home_pos) {

    for(int pos = cur_slider_pos; pos<home_pos;pos++) {
      slider_servo.write(pos);
      cur_slider_pos = pos;
      delay(middle_delay);

    }
  } else {
    for(int pos = cur_slider_pos; pos>home_pos;pos--) {
      slider_servo.write(pos);
      cur_slider_pos = pos;
      delay(middle_delay);
    }
  }
  slider_servo.write(home_pos);              // tell servo to go to position in variable 'pos'
  
    for (int pos = home_pos; pos <home_pos+wiggle_range; pos += 1) { // goes from 180 degrees to 0 degrees
      slider_servo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(middle_delay);                       // waits 15ms for the servo to reach the position
      
    }
    for (int pos = home_pos+wiggle_range; pos >home_pos-wiggle_range; pos -= 1) { // goes from 180 degrees to 0 degrees
      slider_servo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(middle_delay);
   
    }
  for (int pos = home_pos-wiggle_range; pos <home_pos; pos += 1) { // goes from 180 degrees to 0 degrees
    slider_servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(middle_delay);                       // waits 15ms for the servo to reach the position
  
  }
  delay(middle_delay);                       // waits 15ms for the servo to reach the position
  slider_servo.write(home_pos);
  cur_slider_pos = home_pos;
}


void move_slider(int tgt_pos) {
  if(tgt_pos > cur_slider_pos) {
   for(int tmp_pos = cur_slider_pos;tmp_pos < tgt_pos;tmp_pos++) {
    slider_servo.write(tmp_pos); 
   
    delay(move_delay); 
   }
   
  } else {
    for(int tmp_pos = cur_slider_pos;tmp_pos > tgt_pos;tmp_pos--) {
    slider_servo.write(tmp_pos); 
    delay(move_delay); 
    
   }
  }
  slider_servo.write(tgt_pos); 
  cur_slider_pos = tgt_pos;
  //Serial.println(cur_slider_pos);
}

void read_color(boolean debug) {

  uint16_t r,g,b,rt, gt, bt, c;
  tcs.getRawData(&r, &g, &b, &c);

  if(millis()-last_millis > 2000) {
    last_millis = millis();
      Serial.print(r);Serial.print(",");
  Serial.print(g);Serial.print(",");
  Serial.print(b);Serial.print(",");
  Serial.println(cur_slider_pos*10);
  }

}
void scan_color(boolean debug) {
  uint16_t r,g,b, c;
  uint16_t color_sum = 10000000;
  slider_servo.write(home_pos); 
  cur_slider_pos = home_pos;
  if(debug) {
    tcs.getRawData(&r, &g, &b, &c);
      cur_r = r;
      cur_g = g;
      cur_b = b;
      return;
  }
  for(int i=home_pos;i<home_pos+wiggle_range;i++) {
    slider_servo.write(i); 
    cur_slider_pos = i;
    delay(scan_delay);
    tcs.getRawData(&r, &g, &b, &c);
    if((r+g+b)<color_sum) {

      cur_r = r;
      cur_g = g;
      cur_b = b;
      color_sum = r+g+b;
    }
  }
  for(int i=cur_slider_pos;i>home_pos-wiggle_range;i--) {
    delay(scan_delay);
    tcs.getRawData(&r, &g, &b, &c);

    if((r+g+b)<color_sum) {

      cur_r = r;
      cur_g = g;
      cur_b = b;
      color_sum = r+g+b;
    }
    slider_servo.write(i);
    cur_slider_pos = i;
  }
   for(int i=cur_slider_pos;i<home_pos;i++) {
    delay(scan_delay);
    tcs.getRawData(&r, &g, &b, &c);

    if((r+g+b)<color_sum) {

      cur_r = r;
      cur_g = g;
      cur_b = b;
      color_sum = r+g+b;
    }
    slider_servo.write(i);
    cur_slider_pos = i;
  }
  float cur_diff = color_diff(cur_r,cur_g,cur_b,tgt_r,tgt_g,tgt_b);
  Serial.print("Final color: ");
  Serial.print(cur_r);Serial.print(",");
  Serial.print(cur_g);Serial.print(",");
  Serial.print(cur_b);Serial.print(",");
  Serial.print(cur_slider_pos*10);Serial.print(",");
  Serial.println(cur_diff);
  
  
}

void save_color(boolean debug) {
  uint16_t r, g, b, c,color_sum;
  uint16_t rt, gt, bt;
  rt = gt = bt = 0;
  color_sum = 1000000;
  slider_servo.write(home_pos); 
  cur_slider_pos = home_pos;
  if(debug) {
    tcs.getRawData(&r, &g, &b, &c);
          tgt_r = r;
      tgt_g = g;
      tgt_b = b;
      return;
  }
  for(int i=home_pos;i<home_pos+wiggle_range;i++) {
    slider_servo.write(i); 
    cur_slider_pos = i;
    delay(scan_delay);
    tcs.getRawData(&r, &g, &b, &c);
    if((r+g+b)<color_sum) {

      tgt_r = r;
      tgt_g = g;
      tgt_b = b;
      color_sum = r+g+b;
    }
  }
  for(int i=cur_slider_pos;i>home_pos-wiggle_range;i--) {
    delay(scan_delay);
    tcs.getRawData(&r, &g, &b, &c);

    if((r+g+b)<color_sum) {

      tgt_r = r;
      tgt_g = g;
      tgt_b = b;
      color_sum = r+g+b;
    }
    slider_servo.write(i);
    cur_slider_pos = i;
  }
   for(int i=cur_slider_pos;i<home_pos;i++) {
    delay(scan_delay);
    tcs.getRawData(&r, &g, &b, &c);

    if((r+g+b)<color_sum) {

      tgt_r = r;
      tgt_g = g;
      tgt_b = b;
      color_sum = r+g+b;
    }
    slider_servo.write(i);
    cur_slider_pos = i;
  }

  Serial.print("saved current color:");
  Serial.print(tgt_r);Serial.print(",");
  Serial.print(tgt_g);Serial.print(",");
  Serial.print(tgt_b);Serial.print(",");
  Serial.println(cur_slider_pos*10);
 
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
