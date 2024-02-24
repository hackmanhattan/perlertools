#ifndef ColorMath_h
#define ColorMath_h
#include "Arduino.h"
class ColorMath
{
  public:
    ColorMath();
    int get_raw_diff(uint16_t tgt_read_a[], uint16_t tgt_read_b[]);
    double get_cos_dist(uint16_t tgt_read_a[], uint16_t tgt_read_b[]);
    double get_trig_diff(uint16_t tgt_read_a[], uint16_t tgt_read_b[]);
  private:
    bool _debug;
    double get_mag(uint16_t tgt_read_a[]);
    double pairwise_product(uint16_t tgt_read_a[],uint16_t tgt_read_b[]);
};
#endif
