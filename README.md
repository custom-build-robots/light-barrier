# Raspberry Pi - light barrier
I developed a small prototype light barrier to measure the time how long a robot needs to travel through three laser light barriers. I used a Raspberry Pi ZERO W and three laser diodes and three LM393 photo elements to detect if an object is inside the light barrier or not.

![light barrier](https://custom-build-robots.com/wp-content/uploads/2017/12/Raspberry_Pi_Laser_Lichtschranke_Prototyp-300x200.jpg)

## light_barrier.py
The light_barrier.py program ist the easy to use and test program for the light barrier. It only shows how the LM393 photo ellements work together with the Raspberry Pi.

## race_timer.py
The race_timer.py program is more advanced and uses an RFID reader to identify the teams. A Blinkt! eight sement LED strip is used as race timer signal.

## light barrier step by step guide
I published the step by step guide on my blog (for now German only): https://custom-build-robots.com/top-story-de/rundenzeit-messen-raspberry-pi-lichtschranke-einfuehrung/9518
