# BeagleBone web server
# BeagleBone/Debian Linux
#Author: Mohamed Beltagy beltagymohamed@gmail.com

import cherrypy
import os.path
import serial
import time 
import math
import re 

class Server(object):
  preset_value = color_select_value = color_seq_value = GIP_value = direction_value = orientation_value= select_lr_value = freq_value = frame_value = col_value = row_value = wait_cnt_value =''
  preset_value_0 = color_select_value_0 = color_seq_value_0 = GIP_value_0 = direction_value_0 = orientation_value_0= select_lr_value_0 = freq_value_0 = frame_value_0 = col_value_0 = row_value_0 = wait_cnt_value_0 =''
  preset_value_1 = color_select_value_1 = color_seq_value_1 = GIP_value_1 = direction_value_1 = orientation_value_1= select_lr_value_1 = freq_value_1 = frame_value_1 = col_value_1 = row_value_1 = wait_cnt_value_1 =''
  preset_value_2 = color_select_value_2 = color_seq_value_2 = GIP_value_2 = direction_value_2 = orientation_value_2= select_lr_value_2 = freq_value_2 = frame_value_2 = col_value_2 = row_value_2 = wait_cnt_value_2 =''
  col_value_old = row_value_old =  wait_cnt_value_old = save_settings_value = ''
  
  def index(self,preset='',color_select='',color_seq='',GIP='',direction ='',orientation='', select_lr='',freq='',frame='',col='',row='',wait_cnt='',save_settings=''):
    
    ser = serial.Serial('/dev/ttyO0')
    html = open('server.html','r').read()
    
    def chr_data (value):
      str=chr(int(math.floor(value/256)))+chr(int(math.floor((value%256)/16))) +chr(value%16)
      return str
    
    def bchr (value):
      str=chr(int(value,2))
      return str
     
    # this function is used to fix the selection to the last selected 
    def selection (name, value,html) :
      if value!='' and name!='': 
	selection_value= "value='%s'" % value
        selection_name=str(name)
        html=html.replace("%s' selected" %selection_name,"%s'" %selection_name )
	html=html.replace("%s" % selection_value,"%s selected" % selection_value)

        print "selection name ="
        print selection_value
        #print html
        return html
      else:
	return html
      
    

    
    if save_settings != '':
      self.save_settings_value = str(save_settings) 
      if self.save_settings_value[0]== '0':
	self.preset_value_0 = self.preset_value
	self.color_select_value_0 = self.color_select_value
	self.color_seq_value_0 = self.color_seq_value
	self.GIP_value_0 = self.GIP_value
	self.direction_value_0 = self.direction_value
	self.orientation_value_0= self.orientation_value
	self.select_lr_value_0 = self.select_lr_value
	self.freq_value_0 = self.freq_value
	self.frame_value_0 = self.frame_value
	self.col_value_0 = self.col_value
	self.row_value_0 = self.row_value
	self.wait_cnt_value_0 = self.wait_cnt_value
	print"saving settings"	
      elif self.save_settings_value[0] =='1':
	prest= self.preset_value_0
	color_select=self.color_select_value_0
	color_seq=self.color_seq_value_0
	GIP = self.GIP_value_0
	direction = self.direction_value_0
	orientation= self.orientation_value_0
	select_lr = self.select_lr_value_0
	freq= self.freq_value_0
	frame = self.frame_value_0
	col= self.col_value_0
	row= self.row_value_0
	wait_cnt = self.wait_cnt_value_0
      elif self.save_settings_value[0]== '2':
	self.preset_value_1 = self.preset_value
	self.color_select_value_1 = self.color_select_value
	self.color_seq_value_1 = self.color_seq_value
	self.GIP_value_1 = self.GIP_value
	self.direction_value_1 = self.direction_value
	self.orientation_value_1= self.orientation_value
	self.select_lr_value_1 = self.select_lr_value
	self.freq_value_1 = self.freq_value
	self.frame_value_1 = self.frame_value
	self.col_value_1 = self.col_value
	self.row_value_1 = self.row_value
	self.wait_cnt_value_1 = self.wait_cnt_value
	print"saving settings"
      elif self.save_settings_value[0] =='3':
	prest= self.preset_value_1
	color_select=self.color_select_value_1
	color_seq=self.color_seq_value_1
	GIP = self.GIP_value_1
	direction = self.direction_value_1
	orientation= self.orientation_value_1
	select_lr = self.select_lr_value_1
	freq= self.freq_value_1
	frame = self.frame_value_1
	col= self.col_value_1
	row= self.row_value_1
	wait_cnt = self.wait_cnt_value_1
      elif  self.save_settings_value[0] == '4':
	self.preset_value_2 = self.preset_value
	self.color_select_value_2 = self.color_select_value
	self.color_seq_value_2 = self.color_seq_value
	self.GIP_value_2 = self.GIP_value
	self.direction_value_2 = self.direction_value
	self.orientation_value_2= self.orientation_value
	self.select_lr_value_2 = self.select_lr_value
	self.freq_value_2 = self.freq_value
	self.frame_value_2 = self.frame_value
	self.col_value_2 = self.col_value
	self.row_value_2 = self.row_value
	self.wait_cnt_value_2 = self.wait_cnt_value
	print"saving settings"
      elif self.save_settings_value[0]  =='5':
	prest= self.preset_value_2
	color_select=self.color_select_value_2
	color_seq=self.color_seq_value_2
	GIP = self.GIP_value_2
	direction = self.direction_value_2
	orientation= self.orientation_value_2
	select_lr = self.select_lr_value_2
	freq= self.freq_value_2
	frame = self.frame_value_2
	col= self.col_value_2
	row= self.row_value_2
	wait_cnt = self.wait_cnt_value_2
	
    html=selection("_save_settings",self.save_settings_value, html)
    
    
    
    
    preset_value= str(preset)
    if preset_value != '' :
      if preset_value == "0_preset" :
	  
	  ser.write(b'3'+'R' + chr(1) + chr(3) + chr(1) + b';')
	  ser.write(b'3'+'F'+'1'+';')
	  ser.write(b'3'+'S'+'9'+';');
	  ser.write(b'3'+'D' + chr_data(120) + chr_data(160) + ';');
	  ser.write(b'3'+'W' + chr(int('001110',2)) + ';')

      elif  preset_value == "1_preset":
	  # AMLED 120x160 BOT - RGB ROTADED NO GIP
	  ser.write('3' + 'R' + bchr("00000001") + bchr("00000001") + bchr("00000010") + ';')
	  # Set FREQ to 6Mhz
	  ser.write('3' + 'F' + '1' + ';')
	  # 9 Subframes
	  ser.write('3' + 'S' + '9' + ';')
	  ser.write('3' + 'D' + chr_data(120) + chr_data(160) + ';')
	  ser.write('3' + 'W' + bchr("010000") + ';'); # is not yet correct

      elif preset_value == "2_preset":
	  # CPT 240 x 320 GIP GRAY ROTATED
	  ser.write('3' + 'R' + bchr("00001000") + bchr("00000001") + bchr("00000000") + ';')
	  # Set FREQ to 6Mhz
	  ser.write('3' + 'F' + '1' + ';')
	  # 9 Subframes
	  ser.write('3' + 'S' + '9' + ';')
	  ser.write('3' + 'D' + chr_data(240) + chr_data(320) + ';')
	  ser.write('3' + 'W' + bchr("010000") + ';'); # is not yet correct

      elif preset_value== "3_preset" :
	  # QVGA 320 x 240 GRAY
	  ser.write('3' + 'R' + bchr("00000000") + bchr("00000001") + bchr("00000000") + ';')
	  # Set FREQ to 6Mhz
	  ser.write('3' + 'F' + '1' + ';')
	  # 9 Subframes
	  ser.write('3' + 'S' + '9' + ';')
	  ser.write('3' + 'D' + chr_data(320) + chr_data(240) + ';')
	  ser.write('3' + 'W' + bchr("010000") + ';') # is not yet correct
      self.preset_value=str(preset)
    html=selection("_preset_value",self.preset_value, html) 
    
    
    color_select_value=str(color_select)
    if color_select_value != '' :
      if  (color_select_value == '0_color_select'): 
	  ser.write('3' + 'A' + bchr("00000000") + ';')
      elif(color_select_value == '1_color_select'):
	  ser.write('3' + 'A' + bchr("00000001") + ';')
      elif(color_select_value == '2_color_select'):
	  ser.write('3' + 'A' + bchr("00000011") + ';')
      elif(color_select_value == '3_color_select'):
	  ser.write('3' + 'A' + bchr("00000101") + ';')
      elif(color_select_value == '4_color_select'):
	  ser.write('3' + 'A' + bchr("00001001") + ';')
      self.color_select_value=str(color_select)
    html=selection("_color_select_value",self.color_select_value, html)

    
    color_seq_value=str(color_seq)
    if color_seq_value != '':
      if (color_seq_value == '0_color_seq'):
	ser.write('3' + 'B' + bchr("00000000") + ';') 
      elif (color_seq_value == '1_color_seq'):
	ser.write('3' + 'B' + bchr("00000001") + ';') 
      elif (color_seq_value == '2_color_seq'):
	ser.write('3' + 'B' + bchr("00000010") + ';') 
      elif (color_seq_value == '3_color_seq'):
	ser.write('3' + 'B' + bchr("00000011") + ';') 
      elif (color_seq_value == '4_color_seq'):
	ser.write('3' + 'B' + bchr("00000100") + ';') 
      elif (color_seq_value == '5_color_seq'):
	ser.write('3' + 'B' + bchr("00000101") + ';') 
      self.color_seq_value=str(color_seq)
    html=selection("_color_seq",self.color_seq_value, html)
    
    
    if GIP != '':
      self.GIP_value=str(GIP)
      print self.GIP_value
      if self.GIP_value=='0_gip':
	str_sent = '3' + 'G' + chr(0) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
      elif self.GIP_value=='1_gip':
	str_sent = '3' + 'G' + chr(1) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
    html=selection("_gip",self.GIP_value, html)
      
    
    if direction!= '':
      self.direction_value=str(direction)
      if self.direction_value == '0_direction':  
	str_sent = '3' + 'T' + chr(0) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
      elif self.direction_value == '1_direction':
	str_sent = '3' + 'T' + chr(1) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
    html=selection("_direction",self.direction_value, html)
    
    
    if orientation != '':
      self.orientation_value=str(orientation)
      if self.orientation_value == '0_orientation': 
	str_sent = '3' + 'R' + chr(0) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
      elif self.orientation_value == '1_orientation':
	str_sent = '3' + 'R' + chr(1) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
    html=selection("_orientation",self.orientation_value, html)
    
    
    if select_lr != '':
      self.select_lr_value=str(select_lr)
      if self.select_lr_value == '0_select_lr': 
	str_sent = '3' + 'C' + chr(0) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
      elif self.select_lr_value == '1_select_lr':
	str_sent = '3' + 'C' + chr(1) + ';'
	ser.write(str_sent);
	print ("%s") % str_sent
    html=selection("_select_lr",self.select_lr_value, html)
    
    
    if freq != '':
      self.freq_value=str(freq)
      str_sent = '3' + 'F' + chr(int(self.freq_value[0])) + ';'
      ser.write(str_sent)
      print ("%s") % str_sent
    html=selection("_freq",self.freq_value, html)
     
    
    if frame != '':
      self.frame_value=str(frame)
      str_sent = '3' + 'S' + chr(int(self.frame_value[0])) + ';'
      ser.write(str_sent)
      print ("%s") % str_sent
    html=selection("_frame",self.frame_value, html)
   
    
   
    if col != '' and row !='':
      self.col_value=str(col)
      self.row_value=str(row)
      str_sent = '3' + 'D' + chr_data(int(self.col_value)) + chr_data(int(self.row_value))+';'
      ser.write(str_sent);
      print ("col= %d , row = %d") % (int(col) ,int(row))
    html=html.replace("name='col' value='%s'" %  self.col_value_old ,"name='col' value='%s'" % self.col_value)
    html=html.replace("name='row' value='%s'" %  self.row_value_old ,"name='row' value='%s'" % self.row_value)
    
    
    
    if wait_cnt != '':
      self.wait_cnt_value=str(wait_cnt)
      str_sent = '3' + 'W' + chr(int(self.wait_cnt_value)) + ';'
      ser.write(str_sent);
      print ("%s") % str_sent
    html=html.replace("name='wait_cnt' value='%s'" %  self.wait_cnt_value_old ,"name='wait_cnt' value='%s'" % self.wait_cnt_value)
    
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

cherrypy.quickstart(Server(), config=conf)
