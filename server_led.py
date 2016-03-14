# Beagle_Bone_Black
#!/usr/bin/python
# BeagleBone LED web server
# http://aquaticus.info/beaglebone-web-led
# BeagleBone/Angstrom Linux

import cherrypy
import os.path
import serial
import Adafruit_BBIO.GPIO as GPIO
import time 
GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.OUT)
GPIO.setup("P8_14", GPIO.OUT)
class ServerLed(object):
    '''Power ratio in percents. From 0 to 100%'''
    led_power=20 #Initial 20% of power
    '''Switch state 1 (on) or 0 (off)'''
    led_switch=1 #Initial LED on 
    led_value=0  
    led_color=0
    
    def index(self, power='', switch='', value='',color='',data='',preset=''):
        if power:
            self.led_power = ( int(power) / 20 ) * 20
            print "New power %d%%" % self.led_power
            
        if switch:
            self.led_switch = int(switch)
            print "New switch state %d" % self.led_switch
        
	
	self.led_value=value
	print "value = %s  \n " % (self.led_value)

	self.led_color=color
	print "color = %s  \n " % (self.led_color)

	
	def chr(in) 
	    n = int(in, 2)
		return chr(n)
	
	
	if preset != '' :
	    if preset == 1 :
			ser = serial.Serial('/dev/ttyO0')
			ser.write(b'3R' + chr(1) + chr(3) + chr(1) + b';')
            ser.write(b'3F1;')
			ser.write(b'3S9;');
			#ser.write(b'3D' + chr_data(120) + chr_data(160) + ';');
			ser.write(b'3W' + chr("001110") + ';');

		 
		 
	
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
		 
	
		
	if self.led_value== "led0_on":
	    GPIO.output("P8_10", GPIO.HIGH)
	    time.sleep(2)
        elif self.led_value== "led0_off":  
	    GPIO.output("P8_10", GPIO.LOW)
            time.sleep(2)
 	elif self.led_value== "led1_on":  
	    GPIO.output("P8_12", GPIO.HIGH)
            time.sleep(2)
	elif self.led_value== "led1_off":  
	    GPIO.output("P8_12", GPIO.LOW)
            time.sleep(2)
	elif self.led_value== "led2_on":  
	    GPIO.output("P8_14", GPIO.HIGH)
            time.sleep(2)
	elif self.led_value== "led2_off":  
	    GPIO.output("P8_14", GPIO.LOW)
            time.sleep(2)
            
        #read HTML template from file
        html = open('led.html','r').read()

        #replace level bar graph
        level_icon = "level%d.png" % self.led_power
        html = html.replace('level100.png', level_icon)
	
	
        #compute duty cycle based on current power ratio and switch status
        if self.led_switch:
            duty = self.led_power
        else:
            duty = 0 #disable
	

        #pwmSetDutyPercent( duty ) #set PWM duty cycle
        
        #replace bulb icon if LED is disabled (off)
        if not self.led_switch:
            html = html.replace('bulb_on.png', 'bulb_off.png')

        return html

    index.exposed = True

#configuration
conf = {
        'global' : { 
            'server.socket_host': '0.0.0.0', #0.0.0.0 or specific IP
            'server.socket_port': 8080 #server port
        },

        '/images': { #images served as static files
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('images')
        },

        '/favicon.ico': {  #favorite icon
            'tools.staticfile.on': True,  
            'tools.staticfile.filename': os.path.abspath("images/bulb.ico")
        }
    }

cherrypy.quickstart(ServerLed(), config=conf)
