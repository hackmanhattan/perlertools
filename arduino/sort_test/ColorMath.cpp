#include "ColorMath.h"
#include "Arduino.h"
ColorMath::ColorMath() {

}
int ColorMath::get_raw_diff(uint16_t tgt_read_a[], uint16_t tgt_read_b[]) {
  int sum=0;
  for(int i=0;i<10;i++) {
    sum+=abs(tgt_read_a[i]-tgt_read_b[i]);
  }
  return int(sum/8);
}
double ColorMath::get_trig_diff(uint16_t tgt_read_a[], uint16_t tgt_read_b[]) {
  double sum = 0;
  for(int i=0;i<8;i++) {
    sum+= sq(tgt_read_a[i]-tgt_read_b[i]);
  }
  return sqrt(sum);
}
double ColorMath::get_cos_dist(uint16_t tgt_read_a[], uint16_t tgt_read_b[]) { //Thank you M for teaching me how this works
  return abs(1.00 - (pairwise_product(tgt_read_a,tgt_read_b) / (get_mag(tgt_read_a)*get_mag(tgt_read_b))));


  // return pairwise_product(tgt_read_a,tgt_read_b) / (get_mag(tgt_read_a)*get_mag(tgt_read_b));
}

double ColorMath::get_mag(uint16_t tgt_read_a[]) {
  double sum = 0;
  for(int i=0; i<8; i++ ) { 
    sum+= tgt_read_a[i] * tgt_read_a[i];//sq(tgt_read_a[i]);
  }
  return sqrt(sum);
}
double ColorMath::pairwise_product(uint16_t tgt_read_a[],uint16_t tgt_read_b[]){
  double sum = 0;
  for(int i=0;i<8;i++) {
    sum += tgt_read_a[i] * tgt_read_b[i];
  }
  return sum;
}