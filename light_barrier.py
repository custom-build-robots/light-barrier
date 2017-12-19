#!/usr/bin/env python
# coding: latin-1
# Autor:	Ingmar Stapel
# Datum:	20171219
# Version:	1.0
# Homepage:	http://custom-build-robots.com
# This program was developed to measure the time between three .
# light barrier. The program shows how to wait for an GPIO event and 
# how to work with this GPIO event. 
# The program prints the time how long a object needs to move from
# light barrier 1 to the light barrier 3.

import RPi.GPIO as GPIO
import os, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
light_barrier_1 = 13
light_barrier_2 = 19
light_barrier_3 = 26

# Definition of the global variables
global light_barrier_1_time
global light_barrier_2_time
global light_barrier_3_time

light_barrier_1_time = 0.0
light_barrier_2_time = 0.0
light_barrier_3_time = 0.0
	
# The function time_func() calculates the time between the events
# detected if an object travels from the first to the third light
# barrier. 
def time_func(channel):
	global light_barrier_1_time
	global light_barrier_2_time
	global light_barrier_3_time
	if GPIO.input(channel):

		if channel == light_barrier_1:
			light_barrier_1_time = time.time()
			print("Start time measuring:")
		elif channel == light_barrier_2:
			light_barrier_2_time = time.time()
			print("Time section 1: " + str(light_barrier_2_time - light_barrier_1_time))
		elif channel == light_barrier_3:
			light_barrier_3_time = time.time()
			print("Time section 2: " + str(light_barrier_3_time - light_barrier_2_time))
			print("Travel time:    " + str(light_barrier_3_time - light_barrier_1_time))
			
if __name__ == '__main__':
	# Setting the three GPIO pins an IN
	GPIO.setup(light_barrier_1, GPIO.IN)
	GPIO.setup(light_barrier_2, GPIO.IN)
	GPIO.setup(light_barrier_3, GPIO.IN)	

	# Adding the event_detect method to each GPIO pin
	GPIO.add_event_detect(light_barrier_1, GPIO.RISING, callback=time_func, bouncetime=200)
	GPIO.add_event_detect(light_barrier_2, GPIO.RISING, callback=time_func, bouncetime=200)
	GPIO.add_event_detect(light_barrier_3, GPIO.RISING, callback=time_func, bouncetime=200)    
	
	# An active loop to wait for an event.
	try:
		while True:
			time.sleep(0.01)
	except:
		# Cleaning up the GPIO pins and removing the event:
		GPIO.remove_event_detect(light_barrier_1)
		GPIO.remove_event_detect(light_barrier_2)
		GPIO.remove_event_detect(light_barrier_3)		
