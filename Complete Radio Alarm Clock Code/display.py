"""Module that contains the display class for output"""
"""
*    Title: Display Management for Radio Alarm Clock
*    Author: Nicholas McLennan/University of Victoria
*    Date: July 20, 2023
*    Code version: 1.0
"""
#Custom module imports
import constants

# Writing custom fonts and images to screen
from writer import Writer

# For fonts to print to the screen
# For main clock display
import fonts.impact50 as impact50
import fonts.impact16 as impact16
import fonts.impact15 as impact15
# For settings menus
import fonts.arial15 as arial15
import fonts.arial10 as arial10

from icons.icons_matrix import (
    alarm_matrices,
    alarm_big,
    alarm_off,
    volume_up,
    volume_off,
    volume_down,
    settings,
    back_arrow_selector,
    check,
    high_brightness,
    low_brightness,
    star
)
                          
# Helper functions

def convert_to_12hr(hr12_flag, hour):
    """Convert a 24 hour time to a hr12 flag and hr12 time

    Args:
        hr12_flag (bool): indicate if the hr12 setting is on
        hour (int): the current time in 24hr

    Returns:
        tuple(pm_flag, hours): tuple that contains a pm_flag in the first index, and
                               the new 12hr hour in the second index
    """
    # Default to pm
    pm = False
    if hr12_flag is True:
        #If the hour is 0 set it to 12
        if hour == 0:
            
            hours = 12
        # If the hour is greater than or equal to 12, then it is pm
        elif hour >= 12:
            pm = True
            # Convert 24hr to 12hr
            if hour - 12 == 0:
                hours = 12
            else:
                hours = hour - 12
        #If the horu is not greater than or equal to 12, then it is AM.
        else:
            hours = hour
    #  If the hr12 flag is not on, just reply the hours
    else:
        hours = hour
    return [pm, hours]

   
def draw_matrix(matrix, oled, offset_x = 0, offset_y = 0):
    """Draws a matrix to the specified display using pixel()

    Args:
        matrix (list[list]): list that contains what to be printed to display
        oled (SSD1306): display object to print to
        offset_x (int, optional): Offset x to display. Defaults to 0.
        offset_y (int, optional): Offset y to display. Defaults to 0.
    """
    # create offsets
    i = offset_x
    j = offset_y

    # Iterate over each row and column, print the pixel if it is a 1 in the matrix.
    for row_number in range(len(matrix)):
        for column_number in range(len(matrix[row_number])):
            if matrix[row_number][column_number] == 1:
                oled.pixel(i+column_number,j+row_number,1)

class Display():
    """
    Display object class that contains all the methods and data 
    used to control the display output
    """
    def __init__(self):
        """
        Initialize a display object with default settings. 
        It will contain the following:
        - output state 
        - brightness
        - display alarms flag
        - various menu navigation indices.

        """
        # Default Display settings
        self.state = constants.DEFAULT_CLOCK
        self.brightness = 100
        self.display_alarms = True
        # FOR SETTINGS MENU
        self.settings_start_index = 0
        self.settings_active_index = 0
        
        # For Setting Time
        self.selected_time_index = 0
        
        # For Setting Date
        self.selected_date_index = 0
        
        # For Setting Alarms
        self.selected_alarm_weekday_index = 0
        self.selected_alarm_time_index = 0
        
        # For Deleting Alarms
        self.selected_deleted_alarm_index = 0
        
        # For displaying time
        self.hr12 = True
        
    #Brightness Increments
    def increment_brightness(self):
        """Increment the brightness on the display by 10%"""
        if self.brightness != 100:
            self.brightness += 10
    def decrement_brightness(self):
        """Decrement the brightness on the display by 10%"""
        if self.brightness != 0:
            self.brightness -= 10
            
    # Changing Display Format
    def toggle_hour_format(self):
        """Toggle the hour format"""
        self.hr12 = not self.hr12
            
    def increment_active_index(self):
        """Increment the active settings index"""

        # Wrap around if the index is MAX_NUM_SETTINGS to the top of the list
        if self.settings_active_index == constants.MAX_NUM_SETTINGS:
            self.settings_start_index = 0
            self.settings_active_index = 0
        # Otherwise, increment the index
        else:
            self.settings_active_index += 1
            # If the new index is greater than the max number of settings per page, move to the next page
            if (self.settings_active_index - self.settings_start_index) > 2:
                self.settings_start_index = self.settings_active_index
            
            
    def decrement_active_index(self):
        """Decrement the active settings index"""

        # Wrap around if the index is 0 to the bottom of the settings list
        if self.settings_active_index == 0:
            self.settings_start_index = constants.MAX_NUM_SETTINGS-2
            self.settings_active_index = constants.MAX_NUM_SETTINGS
        # Otherwise, increment the index
        else:
            self.settings_active_index -= 1
            # If the new index is on a new page (2,5,8) change the start index to print a new page of settings
            if self.settings_active_index == 5 or self.settings_active_index == 2 or self.settings_active_index == 8:
                self.settings_start_index = self.settings_active_index-2
            
            
    def main_clock_display(self, oled, rtc, radio_channel, clock, hr12 = True, radio = False):
        """Main clock display to display time, date, and radio or alarm informaiton

        Args:
            oled (SSD1306): display object to output to 
            rtc (datetime): datetime object with the current time information
            radio_channel (int): current radio channel
            clock (Clock): clock that contains the alarms
            hr12 (bool, optional): hr12 flag to indicate the format. Defaults to True.
            radio (bool, optional): radio flag to indicate if the radio is active. Defaults to False.
        """
    
        # initialize printers for text
        wri_small = Writer(oled, impact15, verbose = False)
        wri_large = Writer(oled, impact50, verbose = False)
        wri_calendar = Writer(oled, impact16, verbose = False)
        Writer.set_textpos(oled, 0, 0)
        
        pm, hours = convert_to_12hr(hr12, rtc[constants.RTC_HOUR])
        
        # Prep Hour to have correct spacing if it is a single digit
        if len(str(hours)) == 1:
            hours = "  " + str(hours)

        # Print minute   
        wri_large.printstring( str(hours) + ":" + "{:02d}".format(rtc[constants.RTC_MINUTE]))
        # If it is in a 12hr format, print the AM or PM
        if hr12 is True:
            if pm is True:
                wri_small.printstring("PM\n")
            else:
                wri_small.printstring("AM\n")

                
        Writer.set_textpos(oled, 47, 0)
        # Display the current month/day
        wri_calendar.printstring(constants.months[rtc[constants.RTC_MONTH]] + " " + 
                                 str(rtc[constants.RTC_DAY]) + " " + 
                                 constants.days[rtc[constants.RTC_WEEKDAY]])
        # If the radio is active, display it in the bottom right, otherwise display the active alarm
        if radio is True:
            draw_matrix(volume_up, oled, offset_x = 106, offset_y = 26)
            Writer.set_textpos(oled, 47, 75)
            wri_calendar.printstring(str(radio_channel) + "FM")
        elif self.display_alarms is True: # Display Alarms
            # Display only active alarms
            i = 0
            while i <= 2: 
                if clock.alarms[i] is not None and clock.alarms[i].user_enabled is True and clock.alarms[i].initialized is True:
                    draw_matrix(alarm_matrices[i], oled, offset_x = 76+i*15, offset_y = 47)
                i +=1

    def main_settings_display(self, oled, start_index, active_index):
        """Main settings display user interface

        Args:
            oled (SSD1306): display object to output ot 
            start_index (int): index to start displaying from the menu list
            active_index (int): current index the user in on 
        """
        #Initialize text writer and draw a settings icon
        wri_selector = Writer(oled, arial15, verbose= False)
        draw_matrix(settings, oled, offset_x = 110)
        Writer.set_textpos(oled, 0, 0 )
        printing_index = start_index
        
        # Print three setting menus onto the screen, or until the last settings icon is on the screen
        while printing_index <= constants.MAX_NUM_SETTINGS and printing_index <= 2+start_index:
            # If it is the active index, add an arrow to indicate it is 
            if printing_index == active_index:
                line_string = constants.full_list[printing_index]
                wri_selector.printstring(line_string)
                draw_matrix(back_arrow_selector, oled, offset_x = int(len(line_string) * 8), offset_y = (printing_index-start_index)*15)
                wri_selector.printstring("\n")
            # Otherwise, just print the setting menu name
            else:
                line_string = constants.full_list[printing_index] + "\n"
                wri_selector.printstring(line_string)
            printing_index += 1
        
    def volume_display(self, oled, fm_radio_module):
        """Adjust volume display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            fm_radio_module (Radio): Radio object with current volume
        """
        # Initalize object and writers
        fm_radio_settings = fm_radio_module.GetSettings()
        volume = fm_radio_settings[1]
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0, 0)
        # Print the icon based on current volume
        if volume == 0:
            draw_matrix(volume_off, oled, offset_x = 110)
        elif volume < 7:
            draw_matrix(volume_down, oled, offset_x = 110)
        else:
            draw_matrix(volume_up, oled, offset_x = 110)

        # Print out the current volume in text and bar
        wri_text.printstring(f"Volume: {volume}")
        # Have a bar that shows the percentage of volume
        oled.rect(10, 30, 109, 15, 1)
        oled.fill_rect(10, 30, int(1/15*volume * 109), 15, 1)

    def brightness_display(self, oled):
        """Adjust brightness display menu user interface

        Args:
            oled (SSD1306): display object to output to 
        """
        brightness = self.brightness
        # Display the icon in accordance to the current brightness
        if brightness < 50:
            draw_matrix(low_brightness, oled, offset_x = 110)
        else:
            draw_matrix(high_brightness, oled, offset_x = 110)
        # Initialize printer for text
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0, 0)
        # Print out current brightness value
        wri_text.printstring(f"Brightness: {brightness}")
        # Have a bar that shows the percentage of volume
        oled.rect(10, 30, 109, 15, 1)
        oled.fill_rect(10, 30, int(1/100*brightness * 109), 15, 1)
     
    def radio_channel_display(self, oled, fm_radio_module):
        """Radio channel display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            fm_radio_module (Radio): radio object that has current settings
        """
        fm_radio_settings = fm_radio_module.GetSettings()
        frequency = fm_radio_settings[2]
        volume = fm_radio_settings[1]
        mute = fm_radio_settings[0]
        # Print out icon based on the current volume settings
        if mute is False:  
            if volume < 7:
                draw_matrix(volume_down, oled, offset_x = 56, offset_y = 40)
            else:
                draw_matrix(volume_up, oled, offset_x = 56, offset_y = 40)
        else:
            draw_matrix(volume_off, oled, offset_x = 56, offset_y = 40)

        # Initialize printer for current settings
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0, 0)
        # Print out current settings
        wri_text.printstring(f"Channel: {frequency}FM")
        # Have a bar that shows the percentage of volume
        oled.rect(10, 25, 109, 15, 1)
        # Range of 88.0 to 108.0
        oled.fill_rect(10, 25, int(1/(108-88)*(frequency-88) * 109), 15, 1)
        
    def set_time_display(self, oled, clock):
        """Set time display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains current time
        """
        # Contains for where to put the menu title, settings labels,
        # current settings values and selected indicator
        height_row2 = 15
        height_row3 = 30
        height_row4 = 45
        height_row5 = height_row4+2
        #Initalize current time and 12hr format
        datetime = clock.rtc.datetime()
        pm, hours = convert_to_12hr(self.hr12, datetime[constants.RTC_HOUR])

        # Print out title and setting labels
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0,0)
        wri_text.printstring("Set Time")
        Writer.set_textpos(oled, height_row2, 5)
        wri_text.printstring("HH")
        Writer.set_textpos(oled, height_row2, 35)
        wri_text.printstring("MM")
        draw_matrix(check, oled, offset_x = 108, offset_y = height_row3-5)

        #Print out the current setting values
        Writer.set_textpos(oled, height_row3, 7)
        if self.hr12 is True:
            hour_output = hours
        else:
            hour_output = datetime[constants.RTC_HOUR]
        wri_text.printstring("{:02d}".format(hour_output))
        Writer.set_textpos(oled, height_row3, 38)
        wri_text.printstring("{:02d}".format(datetime[constants.RTC_MINUTE]))
        Writer.set_textpos(oled, height_row3, 65)
        # Print out hour format
        if self.hr12 is True:
            wri_text.printstring("12HR")
        else:
            wri_text.printstring("24HR")

        # Print out indicator on current line
        if self.selected_time_index == constants.SET_HOUR:
            oled.hline(5, height_row4, 20, 1)
            
        # Minute
        elif self.selected_time_index == constants.SET_MINUTE:
            oled.hline(35, height_row4, 20, 1)
            
        # 12 vs 24 hr
        elif self.selected_time_index == constants.SET_FORMAT:
            oled.hline(65, height_row4, 40, 1)
        
        else:
            oled.hline(108, height_row4, 20, 1)
        # For AM/PM in timeslot
        if self.hr12 is True:
            wri_12hr = Writer(oled, arial10, verbose=False)
            Writer.set_textpos(oled, height_row5, 8)
            if pm is True:
                wri_12hr.printstring("PM")
            else:
                wri_12hr.printstring("AM")
        
    def set_date_display(self, oled, clock):
        """Set the date display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains the current date
        """
        datetime = clock.rtc.datetime()
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0,0)
        wri_text.printstring("Set Date")
        Writer.set_textpos(oled, 20, 0)
        wri_text.printstring("YYYY")
        Writer.set_textpos(oled, 20, 45)
        wri_text.printstring("MM")
        Writer.set_textpos(oled, 20, 75)
        wri_text.printstring("DD")
        draw_matrix(check, oled, offset_x = 102, offset_y = 35)
        Writer.set_textpos(oled, 40, 2)
        wri_text.printstring("{:04d}".format(datetime[constants.RTC_YEAR]))
        Writer.set_textpos(oled, 40, 48)
        wri_text.printstring("{:02d}".format(datetime[constants.RTC_MONTH]))
        Writer.set_textpos(oled, 40, 78)
        wri_text.printstring("{:02d}".format(datetime[constants.RTC_DAY]))
        
        # Hour
        if self.selected_date_index == 0:
            oled.hline(0, 55, 35, 1)
            
        # Minute
        elif self.selected_date_index == 1:
            oled.hline(45, 55, 20, 1)
            
        # 12 vs 24 hr
        elif self.selected_date_index == 2:
            oled.hline(75, 55, 20, 1)
        
        else:
            oled.hline(100, 55, 20, 1)
            
    def set_alarm_1_weekday_display(self, oled, clock):
        """
        Set alarm 1 display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains alarm 3
        """
        #Initialize writer and pull alarm and 12hr format
        alarm = clock.alarms[0]
        pm, hours = convert_to_12hr(self.hr12, alarm.hour)
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0, 0)
        wri_text.printstring("Set Days")
        # Draw the alarm icon
        draw_matrix(alarm_matrices[0], oled, offset_x = 110)
        # Print the days
        Writer.set_textpos(oled, constants.set_alarm_height_row3, 5)
        wri_text.printstring("M T W R F  S U")
        
        # Print selected days with a star to indicate if it is selected
        i = 0
        while i < len(clock.alarms[0].weekday):
            if clock.alarms[0].weekday[i] is True:
                if i == 0:
                    offset_x = 2
                else:
                    offset_x = i*16
                draw_matrix(star, oled, offset_x = offset_x, offset_y = constants.set_alarm_height_row2)
            i += 1
        
        draw_matrix(check, oled, offset_x = 108, offset_y = constants.set_alarm_height_row3-5)
        
        width = 10
        # Print out selected indicator
        if self.selected_alarm_weekday_index == constants.SET_MONDAY:
            horizontal = 5
        elif self.selected_alarm_weekday_index == constants.SET_TUESDAY:
            horizontal = 20
        elif self.selected_alarm_weekday_index == constants.SET_WEDNESDAY:
            horizontal = 33
            width = 15
        elif self.selected_alarm_weekday_index == constants.SET_THURSDAY:
            horizontal = 53
        elif self.selected_alarm_weekday_index == constants.SET_FRIDAY:
            horizontal = 67
        elif self.selected_alarm_weekday_index == constants.SET_SATURDAY:
            horizontal = 84
        elif self.selected_alarm_weekday_index == constants.SET_SUNDAY:
            horizontal = 98
            
        else:
            horizontal = 110
            width = 20
        
        oled.hline(horizontal, constants.set_alarm_height_row3+15, width, 1)

    def set_alarm_1_time_display(self, oled, clock):
        """
        Set alarm 1 display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains alarm 3
        """
        
        #Initialize writer and pull alarm and 12hr format
        alarm = clock.alarms[0]
        pm, hours = convert_to_12hr(self.hr12, alarm.hour)
        wri_text = Writer(oled, arial15, verbose= False)
        # Draw the alarm icon
        draw_matrix(alarm_matrices[0], oled, offset_x = 110)
        # Draw the options
        Writer.set_textpos(oled, constants.set_alarm_height_row1, 5)
        wri_text.printstring("HH")
        Writer.set_textpos(oled, constants.set_alarm_height_row1, 35)
        wri_text.printstring("MM")
        draw_matrix(check, oled, offset_x = 67, offset_y = constants.set_alarm_height_row2-5)
        #Draw the current information in each option
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 7)
        if self.hr12 is True:
            hour_output = hours
        else:
            hour_output = alarm.hour
        wri_text.printstring("{:02d}".format(hour_output))
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 38)
        wri_text.printstring("{:02d}".format(alarm.minute))
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 69)

        # Print out selected indicator
        if self.selected_alarm_time_index == constants.SET_HOUR:
            oled.hline(5, constants.set_alarm_height_row3, 20, 1)
        elif self.selected_alarm_time_index == constants.SET_MINUTE:
            oled.hline(35, constants.set_alarm_height_row3, 20, 1)
        else:
            oled.hline(67, constants.set_alarm_height_row3, 20, 1)

        # Print out the AM or PM if the user is in 12hr mode
        if self.hr12 is True:
            # Initialize writer
            wri_12hr = Writer(oled, arial10, verbose=False)
            Writer.set_textpos(oled, constants.set_alarm_height_row4, 8)
            # Print out
            if pm is True:
                wri_12hr.printstring("PM")
            else:
                wri_12hr.printstring("AM")

  
    def set_alarm_2_weekday_display(self, oled, clock):
        """
        Set alarm 2 display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains alarm 3
        """
        #Initialize writer and pull alarm and 12hr format
        alarm = clock.alarms[1]
        pm, hours = convert_to_12hr(self.hr12, alarm.hour)
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0, 0)
        wri_text.printstring("Set Days")
        # Draw the alarm icon
        draw_matrix(alarm_matrices[1], oled, offset_x = 110)
        # Print the days
        Writer.set_textpos(oled, constants.set_alarm_height_row3, 5)
        wri_text.printstring("M T W R F  S U")
        
        # Print selected days with a star to indicate if it is selected
        i = 0
        while i < len(clock.alarms[1].weekday):
            if clock.alarms[1].weekday[i] is True:
                if i == 0:
                    offset_x = 2
                else:
                    offset_x = i*16
                draw_matrix(star, oled, offset_x = offset_x, offset_y = constants.set_alarm_height_row2)
            i += 1
        
        draw_matrix(check, oled, offset_x = 108, offset_y = constants.set_alarm_height_row3-5)
        
        width = 10
        # Print out selected indicator
        if self.selected_alarm_weekday_index == constants.SET_MONDAY:
            horizontal = 5
        elif self.selected_alarm_weekday_index == constants.SET_TUESDAY:
            horizontal = 20
        elif self.selected_alarm_weekday_index == constants.SET_WEDNESDAY:
            horizontal = 33
            width = 15
        elif self.selected_alarm_weekday_index == constants.SET_THURSDAY:
            horizontal = 53
        elif self.selected_alarm_weekday_index == constants.SET_FRIDAY:
            horizontal = 67
        elif self.selected_alarm_weekday_index == constants.SET_SATURDAY:
            horizontal = 84
        elif self.selected_alarm_weekday_index == constants.SET_SUNDAY:
            horizontal = 98
            
        else:
            horizontal = 110
            width = 20
        
        oled.hline(horizontal, constants.set_alarm_height_row3+15, width, 1)

    def set_alarm_2_time_display(self, oled, clock):
        """
        Set alarm 2 display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains alarm 3
        """
        
        #Initialize writer and pull alarm and 12hr format
        alarm = clock.alarms[1]
        pm, hours = convert_to_12hr(self.hr12, alarm.hour)
        wri_text = Writer(oled, arial15, verbose= False)
        # Draw the alarm icon
        draw_matrix(alarm_matrices[1], oled, offset_x = 110)
        # Draw the options
        Writer.set_textpos(oled, constants.set_alarm_height_row1, 5)
        wri_text.printstring("HH")
        Writer.set_textpos(oled, constants.set_alarm_height_row1, 35)
        wri_text.printstring("MM")
        draw_matrix(check, oled, offset_x = 67, offset_y = constants.set_alarm_height_row2-5)
        #Draw the current information in each option
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 7)
        if self.hr12 is True:
            hour_output = hours
        else:
            hour_output = alarm.hour
        wri_text.printstring("{:02d}".format(hour_output))
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 38)
        wri_text.printstring("{:02d}".format(alarm.minute))
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 69)

        # Print out selected indicator
        if self.selected_alarm_time_index == constants.SET_HOUR:
            oled.hline(5, constants.set_alarm_height_row3, 20, 1)
        elif self.selected_alarm_time_index == constants.SET_MINUTE:
            oled.hline(35, constants.set_alarm_height_row3, 20, 1)
        else:
            oled.hline(67, constants.set_alarm_height_row3, 20, 1)

        # Print out the AM or PM if the user is in 12hr mode
        if self.hr12 is True:
            # Initialize writer
            wri_12hr = Writer(oled, arial10, verbose=False)
            Writer.set_textpos(oled, constants.set_alarm_height_row4, 8)
            # Print out
            if pm is True:
                wri_12hr.printstring("PM")
            else:
                wri_12hr.printstring("AM")
                
    def set_alarm_3_weekday_display(self, oled, clock):
        """
        Set alarm 3 display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains alarm 3
        """
        #Initialize writer and pull alarm and 12hr format
        alarm = clock.alarms[2]
        pm, hours = convert_to_12hr(self.hr12, alarm.hour)
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0, 0)
        wri_text.printstring("Set Days")
        # Draw the alarm icon
        draw_matrix(alarm_matrices[2], oled, offset_x = 110)
        # Print the days
        Writer.set_textpos(oled, constants.set_alarm_height_row3, 5)
        wri_text.printstring("M T W R F  S U")
        
        # Print selected days with a star to indicate if it is selected
        i = 0
        while i < len(clock.alarms[2].weekday):
            if clock.alarms[2].weekday[i] is True:
                if i == 0:
                    offset_x = 2
                else:
                    offset_x = i*16
                draw_matrix(star, oled, offset_x = offset_x, offset_y = constants.set_alarm_height_row2)
            i += 1
        
        draw_matrix(check, oled, offset_x = 108, offset_y = constants.set_alarm_height_row3-5)
        
        width = 10
        # Print out selected indicator
        if self.selected_alarm_weekday_index == constants.SET_MONDAY:
            horizontal = 5
        elif self.selected_alarm_weekday_index == constants.SET_TUESDAY:
            horizontal = 20
        elif self.selected_alarm_weekday_index == constants.SET_WEDNESDAY:
            horizontal = 33
            width = 15
        elif self.selected_alarm_weekday_index == constants.SET_THURSDAY:
            horizontal = 53
        elif self.selected_alarm_weekday_index == constants.SET_FRIDAY:
            horizontal = 67
        elif self.selected_alarm_weekday_index == constants.SET_SATURDAY:
            horizontal = 84
        elif self.selected_alarm_weekday_index == constants.SET_SUNDAY:
            horizontal = 98
            
        else:
            horizontal = 110
            width = 20
        
        oled.hline(horizontal, constants.set_alarm_height_row3+15, width, 1)

    def set_alarm_3_time_display(self, oled, clock):
        """
        Set alarm 3 display menu user interface

        Args:
            oled (SSD1306): display object to output to 
            clock (Clock): clock object that contains alarm 3
        """
        
        #Initialize writer and pull alarm and 12hr format
        alarm = clock.alarms[2]
        pm, hours = convert_to_12hr(self.hr12, alarm.hour)
        wri_text = Writer(oled, arial15, verbose= False)
        # Draw the alarm icon
        draw_matrix(alarm_matrices[2], oled, offset_x = 110)
        # Draw the options
        Writer.set_textpos(oled, constants.set_alarm_height_row1, 5)
        wri_text.printstring("HH")
        Writer.set_textpos(oled, constants.set_alarm_height_row1, 35)
        wri_text.printstring("MM")
        draw_matrix(check, oled, offset_x = 67, offset_y = constants.set_alarm_height_row2-5)
        #Draw the current information in each option
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 7)
        if self.hr12 is True:
            hour_output = hours
        else:
            hour_output = alarm.hour
        wri_text.printstring("{:02d}".format(hour_output))
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 38)
        wri_text.printstring("{:02d}".format(alarm.minute))
        Writer.set_textpos(oled, constants.set_alarm_height_row2, 69)

        # Print out selected indicator
        if self.selected_alarm_time_index == constants.SET_HOUR:
            oled.hline(5, constants.set_alarm_height_row3, 20, 1)
        elif self.selected_alarm_time_index == constants.SET_MINUTE:
            oled.hline(35, constants.set_alarm_height_row3, 20, 1)
        else:
            oled.hline(67, constants.set_alarm_height_row3, 20, 1)

        # Print out the AM or PM if the user is in 12hr mode
        if self.hr12 is True:
            # Initialize writer
            wri_12hr = Writer(oled, arial10, verbose=False)
            Writer.set_textpos(oled, constants.set_alarm_height_row4, 8)
            # Print out
            if pm is True:
                wri_12hr.printstring("PM")
            else:
                wri_12hr.printstring("AM")
        
    def delete_alarms_display(self, oled, clock):
        """Delete alarms display menu user interface

        Args:
            oled (SSD1306): Display object to output to 
            clock (Clock): clock object that contains the alarm
        """
        # Build output writer
        wri_text = Writer(oled, arial15, verbose= False)
        Writer.set_textpos(oled, 0,0)
        # Main screen information
        wri_text.printstring("Delete Alarms")
        for alarm_id, alarm in enumerate(clock.alarms):
            # For each alarm, if it is enabled and initialized, show that icon
            if alarm.initialized is True and alarm.user_enabled is True: # Alarm is both initialized and enabled
                draw_matrix(alarm_matrices[alarm_id], oled, offset_x = 5 + alarm_id*30, offset_y = 35)
            elif alarm.initialized is True and alarm.user_enabled is False: # Alarm is only initiliazed, but user enabled
                # Crossed out alarm
                draw_matrix(volume_off, oled, offset_x = 5 + alarm_id*30, offset_y = 35)
            else: # alarm is deleted
                draw_matrix(alarm_off, oled, offset_x = 5 + alarm_id*30, offset_y = 35)
                
        # Show the icon to return to home menu
        draw_matrix(check, oled, offset_x = 108, offset_y = 35)

        # Line that shows what the user is currently selecting
        if self.selected_deleted_alarm_index == constants.ALARM_1:
            oled.hline(5, 55, 17, 1)
        elif self.selected_deleted_alarm_index == constants.ALARM_2:
            oled.hline(35, 55, 17, 1)
        elif self.selected_deleted_alarm_index == constants.ALARM_3:
            oled.hline(65, 55, 17, 1)
        else:
            oled.hline(108, 55, 20, 1)


