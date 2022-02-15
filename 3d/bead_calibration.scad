tgt_detail = 720;
screw_d = 2.8;
module screw_holes() {
        translate([-16,0,0])
    union() {
	for (i=[0:2]) {
		translate([0,5+i*30,0])
			cylinder(d=screw_d,h=30,center=true,$fn = tgt_detail);
	}
}
}
module drops() { 
    tgt_height = 100;
    	for (i = [0: 7]) {
		cur_radius = 5.2 + i * 0.2;
		translate([0, 10 * i, tgt_height/4])
			cylinder(d = cur_radius, h = tgt_height, center = true, $fn = tgt_detail);
		translate([5, 10 * i, tgt_height/4])
			cube([10, 1, tgt_height], center = true);
	}

}
module columns() {
	difference() {
	union() {
		translate([-1, 35, 10])
			cube([15, 90, 20], center = true);
		translate([-15, 35, 2])
			cube([15, 90, 4], center = true);
	}
    drops();
	screw_holes();
    }
}
module etext(tgt_text) {
    
      linear_extrude(height = 2) {
            text(str(tgt_text),size=5,font="Arial:style=Bold");
      }
  }
module wheel() {
    degree_diff = 360/8;
    difference() {
        cylinder(d=60,h=5,$fn=tgt_detail,center=true);
        for (i = [0: 7]) {
                   rotate([0,0,i*degree_diff])
            translate([-25,0,0])
            union() {
          
            cur_radius = 5.2 + i * 0.2;
                translate([8,0,2])
                 etext(cur_radius);   
            translate([0, 0, 0])
                cylinder(d = cur_radius, h = 30, center = true, $fn = tgt_detail);
            translate([-5, 0, 0])
                cube([10, 2, 30], center = true);
            }
        }
        cylinder(d=3.4,h=10,center=true,$fn=tgt_detail);
    
   }
}
module gear_center_holes(){
    for (i=[0:7]) {
        translate([25, 10 * i,0])
        cylinder(d=2.8,h=50,center=true,$fn=tgt_detail);
    }
}
module frame() {
    difference() {
        union() {
  	translate([-15, 35, -5])
		cube([15, 90, 10], center = true);
    translate([10,35,-8])
    cube([55,90,4],center=true);
        }
    translate([0,0,-20])
    drops();
    screw_holes();
    gear_center_holes();
    }
}
/*
color([1,0,0])
    columns();
color([0,1,0])
    translate([25,0,-2.5])
    wheel();
*/
color([0,0,1])
    frame();