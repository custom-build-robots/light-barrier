#!/usr/bin/env python
# coding: latin-1
# Autor:	Ingmar Stapel
# Datum:	20171227
# Version:	0.5 beta
# Homepage:	http://custom-build-robots.com
# This program was developed to measure the time between three.
# light barriers. The program shows how to wait for an GPIO event 
# and how to work with this GPIO event. 
# The program prints the time how long a object needs to move from
# light barrier 1 to the light barrier 3.
# A RFID reader is used to identify each time.
# The launch LED is a eight segment Blinkt! led from Pimoroni.

# The program has some problems with fail starts and how to react.
# But most failures are captured and the program is stable enough
# but publish it as an early version 0.5 beta

import RPi.GPIO as GPIO
import os, time

# Import the Blink! library from Pimoroni.
import blinkt
from random import randint
from time import sleep

# To restart / reset the program the advanced python schedulter is 
# used.
from apscheduler.schedulers.background import BackgroundScheduler

# Import the RFID card reader software developed by mxgxw
# and available from GitHub: https://github.com/mxgxw/MFRC522-python
import rfidreader as rfid

import signal

lastcarduid = None
lastcardtime = 0.0

# The BOARD layout is used instead of the BCM layout because the
# RFID reader softwaqre used BOARD. All other programs like Blinkt!
# have to be changed to use also the BOARD layout.
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# The LM393 photo resistors are connected to the pins 33/35/37 
# usind the BOARD layout.
light_barrier_1 = 33
light_barrier_2 = 35
light_barrier_3 = 37

# Definition of the global variables
global light_barrier_1_time
global light_barrier_2_time
global light_barrier_3_time
global continue_reading
global rfid_id
global active_rfid_id
global fail_start
global active_run
global debug

# set the default values for the global variables.
light_barrier_1_time = 0.0
light_barrier_2_time = 0.0
light_barrier_3_time = 0.0
fail_start = False
rfid_id = None
active_rfid_id = None
active_run = False
debug = False

continue_reading = True
	
# The function time_func() calculates the time between the events
# detected if an object travels from the first to the third light
# barrier. 
def time_func(channel):
	global light_barrier_1_time
	global light_barrier_2_time
	global light_barrier_3_time
	global light_barrier_initial_time
	global fail_start
	global active_rfid_id
	global active_run
	check_time = 0.0
	if GPIO.input(channel):
		team = get_team(active_rfid_id)
		if channel == light_barrier_1:
			if light_barrier_1_time == 0.0 and light_barrier_2_time\
			== 0.0 and fail_start == False and rfid_id != None and\
			active_run == True:
				# first measure, no second measure
				light_barrier_1_time = time.time()
				#print("Start time measuring:"+ team)
			elif active_run == False:
				print("!!! FAIL START !!!: "+ team)
				blink_signal("error")				
			elif fail_start == True:
				print("!!! FAIL START !!!: "+ team)
				blink_signal("error")
			elif rfid_id == None:
				fail_start == True
				print("!!! FAIL START rfid id none!!!: ")
				blink_signal("error")

		elif channel == light_barrier_2:
			if light_barrier_1_time > 0.0 and light_barrier_2_time\
			== 0.0:
				light_barrier_2_time = time.time()
		elif channel == light_barrier_3:
			if light_barrier_2_time > 0.0 and light_barrier_3_time\
			== 0.0:
				light_barrier_3_time = time.time()
				
				# use the out function to print / send the values.
				out(team, light_barrier_1_time,\
				light_barrier_2_time, light_barrier_3_time)
				
				# reset the light barrier timer
				light_barrier_1_time = 0.0
				light_barrier_2_time = 0.0
				light_barrier_3_time = 0.0
				active_rfid_id = None
				active_run = False

# The out funtion is used to print or maybe send via Json the
# the data.				
def out(team, time1, time2, time3):
	print("======= "+team+" =======")
	print("Time section 1: " + str(time2 - time1))
	print("Time section 2: " + str(time3 - time2))
	print("Travel time:	" + str(time3 - time1))

# This funktion is used to control the Blinkt! LEDs	
def blink_signal(mode):
	global fail_start
	global light_barrier_1_time
	global active_run
	
	if mode == "read_rfid":
		# start yellow LED to indicate rfid reading
		for i in range(0,8): 
			if fail_start == False:
				blinkt.set_pixel(i,255,255,0)
				blinkt.show()
				sleep(0.05)
			else:
				blink_signal("error")
		# clear the LEDs
		blinkt.clear()
		blinkt.show()
		
	if mode == "search_rfid":
		# start yellow LED to indicate rfid reading
		if debug:
			print "search rfid and fail start: " + str(fail_start)
		if fail_start == False:
			for i in range(0,8): 
				blinkt.set_pixel(i,200,55,0)
				blinkt.show()
				sleep(0.05)
				# clear the LEDs
				blinkt.clear()
				blinkt.show()
		
	elif mode == "countdown" and fail_start == False:
		# start red LED countdown
		if fail_start == False:
			blinkt.set_pixel(0,255,0,0)
			blinkt.set_pixel(1,255,0,0)
			blinkt.show()
			sleep(0.8)
		if fail_start == False:
			blinkt.set_pixel(2,255,0,0)
			blinkt.set_pixel(3,255,0,0)
			blinkt.show()
			sleep(0.8)
		if fail_start == False:
			blinkt.set_pixel(4,255,0,0)
			blinkt.set_pixel(5,255,0,0)
			blinkt.show()
			sleep(0.8)
		if fail_start == False:
			blinkt.set_pixel(6,255,0,0)
			blinkt.set_pixel(7,255,0,0)
			blinkt.show()
			sleep(0.8)
			
	elif mode == "start" and fail_start == False:
		# set all LEDs green
		# print "green"
		active_run = True
		blinkt.set_all(0,100,0)
		blinkt.show()
		sleep(5)
		
	elif mode == "error":
		fail_start = True
		active_run = False

		for i in range(0,20): 
			blinkt.set_all(255,0,0)
			blinkt.show()
			sleep(0.1)
			blinkt.clear()
			blinkt.show()
			sleep(0.1)
		light_barrier_1_time = 0
		fail_start = False
		active_rfid_id = None
		
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	global active_run
	print "Ctrl+C captured, ending read."
	continue_reading = False
	active_run = False
	GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

def restart_timer():
	global active_rfid_id
	global active_run
	active_rfid_id = None
	active_run = False
	if debug:
		print "restart race timer"

# Not very nice but a simple if elif function the get the team
# number from the RFID token ID.
def get_team(value_rfid):
	rfid = value_rfid
	if rfid == "c41072e9":
		team = "Team 1"
	elif rfid == "0faf67d9":
		team = "Team 2"
	else:
		team = "none team found..."
	return team
	
if __name__ == '__main__':
	global light_barrier_initial_time
	light_barrier_initial_time = 0.0

	GPIO.setup(light_barrier_1, GPIO.IN)
	GPIO.setup(light_barrier_2, GPIO.IN)
	GPIO.setup(light_barrier_3, GPIO.IN)	

	# Adding the event_detect method to each GPIO pin
	GPIO.add_event_detect(light_barrier_1, GPIO.RISING,\
	callback=time_func, bouncetime=200)
	GPIO.add_event_detect(light_barrier_2, GPIO.RISING,\
	callback=time_func, bouncetime=200)
	GPIO.add_event_detect(light_barrier_3, GPIO.RISING,\
	callback=time_func, bouncetime=200)	
	
	# An active loop to wait for an event.
	try:
		while continue_reading:

			rfid_id =  rfid.read_rfid()
			if light_barrier_1_time == 0.0 and rfid_id == None and\
			active_rfid_id == None and fail_start == False:
				blink_signal("search_rfid")
				try:
					scheduler.shutdown()
					if debug:
						print "shutdown scheduler..."
				except Exception as e:
					if debug:
						print "Scheduler error: "+e.message

			if light_barrier_1_time == 0 and rfid_id != None:
				active_rfid_id = rfid_id
				blink_signal("read_rfid")
				light_barrier_initial_time = time.time()
				if light_barrier_1_time == 0 and rfid_id != None:
					blink_signal("countdown")
					if light_barrier_1_time == 0 and rfid_id != None:
						active_run = True
						scheduler = BackgroundScheduler()
						scheduler.start()
						scheduler.add_job(restart_timer,'interval',\
						minutes=0.5, id=active_rfid_id)
						if debug:
							print "created scheduler...."
						blink_signal("start")
					else:
						blink_signal("error")
				else:
					blink_signal("error")
				
			if light_barrier_1_time > 0 and active_rfid_id == None:
				blink_signal("error")
				time.sleep(0.1)

	except Exception as e:
		# Cleaning up the GPIO pins and removing the event:
		if debug:
			print e.message
		GPIO.remove_event_detect(light_barrier_1)
		GPIO.remove_event_detect(light_barrier_2)
		GPIO.remove_event_detect(light_barrier_3)		
