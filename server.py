#!/usr/bin/python
# BeagleBone LED web server
# http:#aquaticus.info/beaglebone-web-led
# BeagleBone/Angstrom Linux

import cherrypy
import os.path
import serial
import time 
import math

class ServerLed(object):
 
  
  def index(self,preset='',color_select='',color_seq='',GIP='',direction ='',orientation='', select_lr='',freq='',frame='',col='',row='',wait_cnt=''):
    ser = serial.Serial('/dev/ttyO0')
    
    def chr_data (value):
      str=chr(int(math.floor(value/256)))+chr(int(math.floor((value%256)/16))) +chr(value%16)
      return str
    
    def bchr (value):
      str=chr(int(value,2))
      return str
    

    
    preset_value= str(preset)
    if preset_value != '' :
      if preset_value == "0" :
	  
	  ser.write(b'3'+'R' + chr(1) + chr(3) + chr(1) + b';')
	  ser.write(b'3'+'F'+'1'+';')
	  ser.write(b'3'+'S'+'9'+';');
	  ser.write(b'3'+'D' + chr_data(120) + chr_data(160) + ';');
	  ser.write(b'3'+'W' + chr(int('001110',2)) + ';')

      elif  preset_value == "1":
	  # AMLED 120x160 BOT - RGB ROTADED NO GIP
	  ser.write('3' + 'R' + bchr("00000001") + bchr("00000001") + bchr("00000010") + ';')
	  # Set FREQ to 6Mhz
	  ser.write('3' + 'F' + '1' + ';')
	  # 9 Subframes
	  ser.write('3' + 'S' + '9' + ';')
	  ser.write('3' + 'D' + chr_data(120) + chr_data(160) + ';')
	  ser.write('3' + 'W' + bchr("010000") + ';'); # is not yet correct

      elif preset_value == "2":
	  # CPT 240 x 320 GIP GRAY ROTATED
	  ser.write('3' + 'R' + bchr("00001000") + bchr("00000001") + bchr("00000000") + ';')
	  # Set FREQ to 6Mhz
	  ser.write('3' + 'F' + '1' + ';')
	  # 9 Subframes
	  ser.write('3' + 'S' + '9' + ';')
	  ser.write('3' + 'D' + chr_data(240) + chr_data(320) + ';')
	  ser.write('3' + 'W' + bchr("010000") + ';'); # is not yet correct

      elif preset_value== "3" :
	  # QVGA 320 x 240 GRAY
	  ser.write('3' + 'R' + bchr("00000000") + bchr("00000001") + bchr("00000000") + ';')
	  # Set FREQ to 6Mhz
	  ser.write('3' + 'F' + '1' + ';')
	  # 9 Subframes
	  ser.write('3' + 'S' + '9' + ';')
	  ser.write('3' + 'D' + chr_data(320) + chr_data(240) + ';')
	  ser.write('3' + 'W' + bchr("010000") + ';') # is not yet correct

    color_select_value=str(color_select)
    if color_select_value != '' :
      if  (color_select_value == '0'): 
	  ser.write('3' + 'A' + bchr("00000000") + ';')
      elif(color_select_value == '1'):
	  ser.write('3' + 'A' + bchr("00000001") + ';')
      elif(color_select_value == '2'):
	  ser.write('3' + 'A' + bchr("00000011") + ';')
      elif(color_select_value == '3'):
	  ser.write('3' + 'A' + bchr("00000101") + ';')
      elif(color_select_value == '4'):
	  ser.write('3' + 'A' + bchr("00001001") + ';')

    color_seq_value=str(color_seq)
    if color_seq_value != '':
      if (color_seq_value == '0'):
	ser.write('3' + 'B' + bchr("00000000") + ';') 
      elif (color_seq_value == '1'):
	ser.write('3' + 'B' + bchr("00000001") + ';') 
      elif (color_seq_value == '2'):
	ser.write('3' + 'B' + bchr("00000010") + ';') 
      elif (color_seq_value == '3'):
	ser.write('3' + 'B' + bchr("00000011") + ';') 
      elif (color_seq_value == '4'):
	ser.write('3' + 'B' + bchr("00000100") + ';') 
      elif (color_seq_value == '5'):
	ser.write('3' + 'B' + bchr("00000101") + ';') 
    
    GIP_value=str(GIP)
    if GIP_value != '':
      str_sent = '3' + 'G' + chr(int(GIP)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
      
    direction_value=str(direction)
    if direction_value != '':
      str_sent = '3' + 'T' + chr(int(direction)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
    
    
    if orientation != '':
      str_sent = '3' + 'R' + chr(int(orientation)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
    
    if select_lr != '':
      str_sent = '3' + 'C' + chr(int(select_lr)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
    
    if freq != '':
      str_sent = '3' + 'F' + chr(int(freq)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
      
    if frame != '':
      str_sent = '3' + 'S' + chr(int(frame)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
   
    if col != '' and row !='':
      str_sent = '3' + 'D' + chr_data(int(col)) + chr_data(int(row))+';'
      ser.write(str_sent);
      print ("col=%d, row = %d") % (int(col) ,int(row))
    
    if wait_cnt != '':
      str_sent = '3' + 'W' + chr(int(wait_cnt)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
	
    #read HTML template from file
    html = open('server.html','r').read()

    
    

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
        }
    }

cherrypy.quickstart(ServerLed(), config=conf)
