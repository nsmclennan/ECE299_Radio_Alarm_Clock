"""
*    Title: Main Script for Radio Alarm Clock
*    Author: Nicholas McLennan
*    Date: July 20, 2023
*    Code version: 1.0
"""

# NOTES:

# Multiple days for one alarm
# Possibly print each alarm day if adding multiple days to one alarm    

# Custom module imports
import constants
from icons.icons_matrix import (
    alarm_big,
)
from display import Display, draw_matrix
from clock import Clock, check_alarms
from buttons import update_display_state

# For core interaction with the Raspberry Pico
from machine import Pin, I2C, Timer, SPI, RTC, PWM
import utime

# For radio and display modules
from fm_radio import Radio
from ssd1306 import SSD1306_SPI # this is the driver library and the corresponding class
import framebuf # this is another library for the display. 

def play_alarm(alarm_output, delay):
    """Play the alarm periodically without interrupting the rest of the running code

    Args:
        alarm_output (PWM): PWM object to output audio to
        delay (int): period of audio
    """

    # Set global variables for next time entering the function
    global last_time_sound, pulse_number

    # Get the current time
    new_time = utime.ticks_ms()
    
    # If the time since the last change was greater than delay ms
    if new_time - last_time_sound > delay:
        # Update the last time, and return a valid press.
        last_time_sound = new_time
        
        current_duty = alarm_output.duty_u16()
        if current_duty == 0:
            alarm_output.duty_u16(constants.pulse_duty[pulse_number])
        else:
            alarm_output.duty_u16(0)
            pulse_number += 1
            if pulse_number >= constants.MAX_NUM_ALARM_NOTES:
                pulse_number = 0
        
        alarm_output.freq(constants.pulse_freq[pulse_number])


def wait_for_single_button_press(pin):
    """Wait for a single button press

    Args:
        pin (Pin): pin object that the button was pressed on 

    Returns:
        bool: indicate if a button press has occured.
    """

    # Set global variables for next time entering the function
    global last_time

    # Get the current time
    new_time = utime.ticks_ms()
    
    # If the time since the last press was greater than 100 ms
    if new_time - last_time > 150:
        # Update the last time, and return a valid press.
        last_time = new_time
        return True
    return False

# IRQ Functions for Button Definitions
def button_1_callback(pin):
    
    """Function called if a button 1 input is recieved"""
    # Wait for a single press to debounce
    if wait_for_single_button_press(pin):
        update_display_state(1, display, clock, fm_radio_module, alarm_output)

def button_2_callback(pin):
    """Function called if a button 2 input is recieved"""
    # Wait for a single press to debounce
    if wait_for_single_button_press(pin):
        update_display_state(2, display, clock, fm_radio_module, alarm_output)
    
def button_3_callback(pin):
    """Function called if a button 3 input is recieved"""
    # Wait for a single press to debounce
    if wait_for_single_button_press(pin):
        update_display_state(3, display, clock, fm_radio_module, alarm_output)

def button_4_callback(pin):
    """Function called if a button 4 input is recieved"""
    # Wait for a single press to debounce
    if wait_for_single_button_press(pin):
        update_display_state(4, display, clock, fm_radio_module, alarm_output)
        
# Button Definitions For UI
button_1 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
button_4 = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

# IRQ Definitions
button_1.irq(trigger=machine.Pin.IRQ_RISING, handler=button_1_callback)
button_2.irq(trigger=machine.Pin.IRQ_RISING, handler=button_2_callback)
button_3.irq(trigger=machine.Pin.IRQ_RISING, handler=button_3_callback)
button_4.irq(trigger=machine.Pin.IRQ_RISING, handler=button_4_callback)

# Initialize radio module for fm radio
fm_radio_module = Radio(100.3, 7, True)

#Initialize display object that encapsulates the user interface algorithm
display = Display()

# Define columns and rows of the oled display. These numbers are the standard values. 
SCREEN_WIDTH = 128 #number of columns
SCREEN_HEIGHT = 64 #number of rows

spi_sck = Pin(18) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
spi_sda = Pin(19) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
spi_res = Pin(21) # res stands for reset; to be connected to a free GPIO pin
spi_dc  = Pin(20) # dc stands for data/command; to be connected to a free GPIO pin
spi_cs  = Pin(17) # chip select; to be connected to the SPI chip select of the Pico

# SPI Device ID can be 0 or 1. It must match the wiring. 
SPI_DEVICE = 0 # Because the peripheral is connected to SPI 0 hardware lines of the Pico

# Initialize the SPI interface for the OLED display
oled_spi = SPI( SPI_DEVICE, baudrate= 100000, sck= spi_sck, mosi= spi_sda )

# Initialize the display
oled = SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )

# Initialize Variables for Debounce
last_time = 0

# Initialize the clock for alarms and rtc time control 
clock = Clock()

# Set default values for alarms that the user can edit
clock.set_alarm(0, constants.empty_alarm_weekdays_1, 0, 0)
clock.set_alarm(1, constants.empty_alarm_weekdays_2, 0, 0)
clock.set_alarm(2, constants.empty_alarm_weekdays_3, 0, 0)

# Initialize PWM for alarm
alarm_output = PWM(Pin(15))
alarm_output.duty_u16(0)

# Initialization for periodic functions
last_time_sound = 0
pulse_number = 0
last_time_snooze = 0


# Ensure the alarm is not playing when turned off
def reset_alarm(pin):
    """Function to call to ensure the alarm is not playing any audio"""
    if display.state != constants.ALARM_OFF:
        if alarm_output.duty_u16() != 0:
            alarm_output.duty_u16(0)

# Timer reset alarm periodically
alarm_timer = Timer()
alarm_timer.init(mode=Timer.PERIODIC, freq = 100, callback=reset_alarm)

# Snooze alarm periodically
def snooze_alarm(pin):
    """Function to snooze the alarm"""
    if clock.alarm_triggered is True:
        if display.state == constants.ALARM_OFF:
            display.state = constants.DEFAULT_CLOCK
        else:
            display.state = constants.ALARM_OFF

# Snooze alarm periodically
snooze_timer = Timer()
snooze_timer.init(mode=Timer.PERIODIC, freq = 1/60, callback=snooze_alarm)


while True:
    # Clear Buffer
    oled.fill(0)

    # Update display brightness based on user setting
    oled.contrast(int(display.brightness/100*255))
    
    # Check if any alarms should go off
    if check_alarms(clock, display):
        display.state = constants.ALARM_OFF
        
    # Update display data depending on current state
    if display.state == constants.DEFAULT_CLOCK:
        display.main_clock_display(oled, clock.rtc.datetime(), fm_radio_module.GetSettings()[2], clock, hr12 = display.hr12, radio = not fm_radio_module.GetSettings()[0])
        
    elif display.state == constants.MAIN_MENU:
        display.main_settings_display(oled, display.settings_start_index, display.settings_active_index)
        
    elif display.state == constants.ADJUST_TIME_MENU:
        display.set_time_display(oled, clock)
        
    elif display.state == constants.ADJUST_DATE_MENU:
        display.set_date_display(oled, clock)

    elif display.state == constants.SET_ALARM_1_WEEKDAY:
        display.set_alarm_1_weekday_display(oled, clock)
    
    elif display.state == constants.SET_ALARM_1_TIME:
        display.set_alarm_1_time_display(oled, clock)

    elif display.state == constants.SET_ALARM_2_WEEKDAY:
        display.set_alarm_2_weekday_display(oled, clock)
    
    elif display.state == constants.SET_ALARM_2_TIME:
        display.set_alarm_2_time_display(oled, clock)

    elif display.state == constants.SET_ALARM_3_WEEKDAY:
        display.set_alarm_3_weekday_display(oled, clock)
    
    elif display.state == constants.SET_ALARM_3_TIME:
        display.set_alarm_3_time_display(oled, clock)
    
    elif display.state == constants.DELETE_ALARMS:
        display.delete_alarms_display(oled, clock)
    
    elif display.state == constants.CHANGE_FM_STATION_MENU:
        display.radio_channel_display(oled, fm_radio_module)
        
    elif display.state == constants.BRIGHTNESS_MENU:
        display.brightness_display(oled)
        
    elif display.state == constants.VOLUME_MENU:
        display.volume_display(oled, fm_radio_module)
        
    elif display.state == constants.ALARM_OFF:
        # Set the alarm off for periodic snooze 
        clock.alarm_triggered = True 
        # If the radio module is not muted, take note to resume playing after the alarm is muted
        if fm_radio_module.Mute is False:
            fm_radio_module.SetMute(True)
            fm_radio_module.ProgramRadio()
            fm_radio_module.radio_module_previously_on = True
        
        # The actual display/audio output
        draw_matrix(alarm_big, oled, offset_x=32)
        play_alarm(alarm_output, 75)
                    
            
        
    # Transfer buffer to screen
    oled.show()


