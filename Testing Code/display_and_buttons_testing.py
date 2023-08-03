"""
*    Title: Display and Buttons Testing for Radio Alarm Clock
*    Author: Nicholas McLennan/Alex Rockson/University of Victoria
*    Date: July 4, 2023
*    Code version: 1.0
"""
from machine import Pin, SPI # SPI is a class associated with the machine library. 
import utime

# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
from ssd1306 import SSD1306_SPI # this is the driver library and the corresponding class
import framebuf # this is another library for the display. 


# Define columns and rows of the oled display. These numbers are the standard values. 
SCREEN_WIDTH = 128 #number of columns
SCREEN_HEIGHT = 64 #number of rows


# Initialize I/O pins associated with the oled display SPI interface

spi_sck = Pin(18) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
spi_sda = Pin(19) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
spi_res = Pin(21) # res stands for reset; to be connected to a free GPIO pin
spi_dc  = Pin(20) # dc stands for data/command; to be connected to a free GPIO pin
spi_cs  = Pin(17) # chip select; to be connected to the SPI chip select of the Pico 

#
# SPI Device ID can be 0 or 1. It must match the wiring. 
#
SPI_DEVICE = 0 # Because the peripheral is connected to SPI 0 hardware lines of the Pico

#
# initialize the SPI interface for the OLED display
#
oled_spi = SPI( SPI_DEVICE, baudrate= 100000, sck= spi_sck, mosi= spi_sda )

#
# Initialize the display
#
oled = SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )
#
# Initialize the button
#
button_1 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
button_4 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

# Set count to 0
Count = 0

while ( True ):
    
#
# Button debounce method
#
        # Check if the button_1 is pressed
        if(button_1.value() == 0):
            # Wait for x ms
            utime.sleep(0.005)
            # If it is still pressed, increment counter
            if(button_1.value() == 0):
                Count+=1
        # Wait until the button is no longer pressed
        while(button_1.value() == 0):
            pass
        # Check if the button_2 is pressed
        if(button_2.value() == 0):
            # Wait for x ms
            utime.sleep(0.005)
            # If it is still pressed, increment counter
            if(button_2.value() == 0):
                Count+=1
        # Wait until the button is no longer pressed
        while(button_2.value() == 0):
            pass        
        
        # Check if the button_3 is pressed
        if(button_3.value() == 0):
            # Wait for x ms
            utime.sleep(0.005)
            # If it is still pressed, increment counter
            if(button_3.value() == 0):
                Count+=1
        # Wait until the button is no longer pressed
        while(button_3.value() == 0):
            pass


        # Check if the button_4 is pressed
        if(button_4.value() == 0):
            # Wait for x ms
            utime.sleep(0.005)
            # If it is still pressed, increment counter
            if(button_4.value() == 0):
                Count+=1
        # Wait until the button is no longer pressed
        while(button_4.value() == 0):
            pass
#
# Clear the buffer
#
        oled.fill(0)
        
#
# Update the text on the screen
#
        oled.text("Welcome to ECE", 0, 0) # Print the text starting from 0th column and 0th row
        oled.text("299", 45, 10) # Print the number 299 starting at 45th column and 10th row
        oled.text("Count is: %4d" % Count, 0, 30 ) # Print the value stored in the variable Count. 
        
#
# Draw box below the text
#
        oled.rect( 0, 50, 128, 5, 1  )        

#
# Transfer the buffer to the screen
#
        oled.show()
    