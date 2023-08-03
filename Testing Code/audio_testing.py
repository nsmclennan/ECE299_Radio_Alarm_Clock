"""
*    Title: Audio Testing for Radio Alarm Clock
*    Author: Nicholas McLennan/Alex Rockson
*    Date: July 30, 2023
*    Code version: 1.0
"""

from machine import Pin, PWM
from utime import sleep
import utime

# Define radio
alarm_output = PWM(Pin(5))
alarm_output.duty_u16(0)

last_time = 0

import random

def play_pulse(alarm_output, freq, duty, delay):
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
    if new_time - last_time > delay:
        # Update the last time, and return a valid press.
        last_time = new_time
        freq_new = random.randint(0,1)
        current_duty = alarm_output.duty_u16()
        if current_duty == 0:
            if freq_new == 0:
                alarm_output.duty_u16(duty)
            else:
                alarm_output.duty_u16(256)
        else:
            alarm_output.duty_u16(0)
        
        if freq_new == 0:
            alarm_output.freq(freq)
        else:
            alarm_output.freq(750)
        
    return False

while True:
    play_pulse(alarm_output, 500, 512, 100)
    
