#!/usr/bin/python
# 7seg.py
# routines to drive the sparkfun i2c 7 segment display
# This is the syntax:  bus.write_byte_data(address,register,value)
# Or, to read values back:  value =  bus.read_byte_data(address,register) 
# to get i2c working, remove i2c from the blacklist file.
# Then add i2c-dev to /etc/modules
# sudo adduser pi i2c
# then reboot
# sudo i2cdetect -y 1    --- will show the map of detected devices

import time
import smbus
import logging
import datetime
#import sys
#import getopt
#import os
 
bus = smbus.SMBus(1) # For revision 1 Raspberry Pi, change to bus = smbus.SMBus(1) for revision 2.
address = 0x20 			# i2C address of MCP23017
sevensegaddress=0x77	# i2c address of 7segment display
# this address above can get changed by sw glitch. It started at 0x71.
#registera = 0x12
#registerb = 0x13
# decide how bright we want it
defaultbrightness=255
#constants for the sparkfun 7 seg dsplay
cleardisplay=0x76		#followed by nothing
decimalcontrol=0x77		#followed by 0-63
cursorcontrol=0x79		#followed by 0-3
brightnesscontrol=0x7A	#followed by 0-255
digit1control=0x7B
digit2control=0x7C
digit3control=0x7D
digit4control=0x7E
baudrateconfig=0x7F
i2caddressconfig=0x80
factoryreset=0x81
LOGFILE = '/home/pi/python-spi/log/7seg.log'

class sevenseg:
	'''7 segment control.'''
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.ioerrorcount = 0
	try:
		bus.write_byte(sevensegaddress,cleardisplay)
		bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
		time.sleep(1)
		bus.write_byte(sevensegaddress,0)	#draw colon
		time.sleep(1)
		bus.write_byte(sevensegaddress,1)	#draw colon
		time.sleep(1)
		bus.write_byte(sevensegaddress,2)	#draw colon
		time.sleep(1)
		bus.write_byte(sevensegaddress,3)	#draw colon
	except IOError:
		self.ioerrorcount = self.ioerrorcount + 1
		logging.warning('IO error in init')
		#print "IO error in init: " , self.ioerrorcount

	def updateclock(self):
	  timenow=list(time.localtime())
	  hour=timenow[3]
	  minute=timenow[4] 
	  #print "Updating clock:- ", hour, ":",minute
	  logging.warning("updating clock"+str(timenow))
	  try:  
		bus.write_byte(sevensegaddress,cleardisplay)
		bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
		bus.write_byte(sevensegaddress,int(hour/10))
		bus.write_byte(sevensegaddress,hour%10)
		bus.write_byte(sevensegaddress,int(minute/10))
		bus.write_byte(sevensegaddress,minute%10)
		return(0)
	  except IOError:
		self.ioerrorcount = self.ioerrorcount + 1
		# need to reset cursor position when this happens
		#print "Error writing to 7segment display:", self.ioerrorcount 
		logging.warning('error writing to 7seg display')
		time.sleep(1)
		bus.write_byte(sevensegaddress,cleardisplay)
		time.sleep(1)
		return(1)
	
	def write7seg(self,value):
	  try:  
		bus.write_byte(sevensegaddress,cleardisplay)
	#    bus.write_byte_data(sevensegaddress,decimalcontrol,16)	#draw colon
		bus.write_byte(sevensegaddress,value/10)
		bus.write_byte(sevensegaddress,hour%10)
		bus.write_byte(sevensegaddress,int(minute/10))
		bus.write_byte(sevensegaddress,minute%10)
	  except IOError:
		self.ioerrrocount = self.ioerrorcount + 1
		#print "Error writing to 7segment display: ", self.ioerrorcount  
		initclock()  

	def dimdisplay(self,brightness):
	  # max brightness=255
	  #print "Dimming 7 segment display=",brightness
	  try:  
		bus.write_byte_data(sevensegaddress,brightnesscontrol,brightness)
	  except IOError:
		self.ioerrorcount = self.ioerrorcount + 1
		#print "Error writing to 7segment display: ", self.ioerrorcount  
		
  ##The start of the real code ##
if __name__ == "__main__":
	#print "Running 7seg class as a standalone app"
	logging.basicConfig(filename=LOGFILE,
						filemode='w',
						level=logging.INFO)	#filemode means that we do not append anymore
#	Default level is warning, level=logging.INFO log lots, level=logging.DEBUG log everything
	logging.warning(datetime.datetime.now().strftime('%d %b %H:%M')+". Running 7seg class as a standalone app")
	my7seg = sevenseg()
	time.sleep(5)		#let the board settle down
	while True:
		if my7seg.updateclock() == 0:
			my7seg.dimdisplay(defaultbrightness)
			time.sleep(30)
		