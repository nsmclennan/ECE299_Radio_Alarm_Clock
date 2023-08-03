"""
*    Title: Clock and Alarm Management for Radio Alarm Clock
*    Author: Nicholas McLennan
*    Date: July 20, 2023
*    Code version: 1.0
"""
import constants
from machine import RTC

# Helper Functions
def check_alarms(clock, display):
    """Check if there are any alarms to be triggered and triggers them.

    Args:
        clock (RTC): rtc object that holds the current time
        display (Display): display object that contains the current state
    """
    # Create a list of the dates to be comapred against for the active alarm
    date_list = [clock.rtc.datetime()[constants.RTC_WEEKDAY], clock.rtc.datetime()[constants.RTC_HOUR], clock.rtc.datetime()[constants.RTC_MINUTE]]
    sound_alarm = False
    for alarm in clock.alarms:
        # For each alarm, ensure it is created, then compare it's trigger date to the current date
        if alarm is not None:
            # The weekday is pulled from the list of weekdays, if it is valid at the same weekday in the date list will be true
            alarm_list = [alarm.weekday[date_list[0]], alarm.hour, alarm.minute]
            # Trigger the alarm if it is the correct time
            if alarm_list[1] == date_list[1] and alarm_list[2] == date_list[2] and alarm_list[0] is True and not alarm.triggered and alarm.user_enabled and alarm.initialized:
                # Don't trigger alarm while changing settings
                if display.state != constants.ADJUST_TIME_MENU and display.state != constants.ADJUST_DATE_MENU:
                    sound_alarm = True
                    alarm.triggered = True
            # Reset the alarm if triggered by comparing the minute values from alarm and current clock
            if alarm_list[2] != date_list[2] and alarm.triggered:
                alarm.triggered = False
    return sound_alarm

def check_leap_year(year) -> bool:
    """Check if the input year is a leap year

    Args:
        year (int): input year

    Returns:
        bool: True if it is a leap year, false if not
    """
    return year % 4 == 0 and ( year % 100 != 0 or year % 400 == 0)

class Alarm():
    def __init__(self, year, month, day, weekday, hour, minute, triggered):
        """Initialize the alarm object with the time specifications, triggered and enable"""
        self.year = year
        self.month = month
        self.day = day
        self.weekday = weekday
        self.hour = hour
        self.minute = minute
        self.triggered = triggered
        self.user_enabled = True
        self.initialized = False
    
    def add_weekday(self, weekday_number):
        """Add weekday to the alarm"""
        self.weekday[weekday_number] = True
        
    def remove_weekday(self, weekday_number):
        """Remove weekday from alarm"""
        self.weekday[weekday_number] = False
    
        
    def toggle_user_enable(self):
        """Toggle the user enable or mute the alarm temporarily"""
        self.user_enabled = not self.user_enabled
        
    def toggle_initialize(self):
        """Toggle the initialization to delete the alarm"""
        self.initialized = not self.initialized
        
        
    def increment_hour(self):
        """Increment the hour set for the alarm"""
        if self.hour + 1 >= 24:
            self.hour = 0
        else:
            self.hour = self.hour + 1
    
    def increment_minute(self):
        """Increment the minute set for the alarm"""
        if self.minute + 1 >= 60:
            self.minute = 0
        else:
            self.minute = self.minute + 1

        
    def decrement_hour(self):
        """Decrement the hour set for the alarm"""
        if self.hour - 1 < 0:
            self.hour = 23
        else:
            self.hour = self.hour - 1
    
    def decrement_minute(self):
        """Decrement the minute set for the alarm"""
        if self.minute - 1 < 0:
            self.minute = 59
        else:
            self.minute = self.minute - 1
            
    
            
class Clock():
    def __init__(self):
        """Initialize the clock object with an rtc counter, set the datetime, and three alarms"""
        self.rtc = RTC()
        # Initialization date doesn't matter, just selected a random date
        self.rtc.datetime((2023, 8, 30, constants.WEDNESDAY, 3, 22, 55, 0))
        self.alarms = [None, None, None]
        self.alarm_triggered = False
    
    def set_alarm(self, alarm_number, weekday, hour, minute):
        # Add an Alarm object to the alarm list
        self.alarms[alarm_number] = Alarm(self.rtc.datetime()[constants.RTC_YEAR], 
                                          self.rtc.datetime()[constants.RTC_MONTH], 
                                          self.rtc.datetime()[constants.RTC_DAY], 
                                          weekday, hour, minute, False)

    def increment_year(self):
        """Increment the year in the rtc counter"""
        current_datetime = self.rtc.datetime()
        # Try to increase the year, if it is invalid, an OSError is thrown, then reset year to 0
        try:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_YEAR] = current_datetime[constants.RTC_YEAR] + 1
            self.rtc.datetime(tuple(current_datetime_list))
        except OSError:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_YEAR] = 0
            self.rtc.datetime(tuple(current_datetime_list))
        
    def increment_month(self):
        """Increment month in the rtc, with valid day correction"""
        current_datetime = self.rtc.datetime()
        current_datetime_list = list(current_datetime)

        # Adjust Month
        if current_datetime_list[constants.RTC_MONTH] + 1 > 12:
            current_datetime_list[constants.RTC_MONTH] = 1
        else:
            current_datetime_list[constants.RTC_MONTH] = current_datetime_list[constants.RTC_MONTH] + 1
        # Adjust day if necessary, ensuring the days match up if leap year    
        if check_leap_year(current_datetime_list[constants.RTC_YEAR]):
            real_days_in_month = constants.days_in_month_leap[current_datetime_list[constants.RTC_MONTH]]             
        else:
            real_days_in_month = constants.days_in_month[current_datetime_list[constants.RTC_MONTH]]
        
        if current_datetime_list[constants.RTC_DAY] > real_days_in_month:
            # Update the day
            current_datetime_list[constants.RTC_DAY] = real_days_in_month 

        #Update the time                                                                                                                                 
        self.rtc.datetime(tuple(current_datetime_list))
        
    def increment_day(self):
        """Increment the day in the rtc counter, with validation correction"""
        current_datetime = self.rtc.datetime()
        current_datetime_list = list(current_datetime)

        # Check for leap year
        if check_leap_year(current_datetime_list[constants.RTC_YEAR]):
            real_days_in_month = constants.days_in_month_leap[current_datetime_list[constants.RTC_MONTH]]             
        else:
            real_days_in_month = constants.days_in_month[current_datetime_list[constants.RTC_MONTH]]
        
        # Adjust day
        if current_datetime_list[constants.RTC_DAY] + 1 > real_days_in_month:
            current_datetime_list[constants.RTC_DAY] = 1
        else:
            current_datetime_list[constants.RTC_DAY] = current_datetime_list[constants.RTC_DAY] + 1

        # Update the time
        self.rtc.datetime(tuple(current_datetime_list))
            
    def increment_hour(self):
        """Increment hour counter in rtc"""
        current_datetime = self.rtc.datetime()
        # Try to increase the day, if it is invalid, an OSError is thrown, then reset day to 0
        try:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_HOUR] = current_datetime[constants.RTC_HOUR] + 1
            self.rtc.datetime(tuple(current_datetime_list))
        except OSError:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_HOUR] = 0
            self.rtc.datetime(tuple(current_datetime_list))

    def increment_minute(self):
        """Increment minute counter in rtc"""
        current_datetime = self.rtc.datetime()
        # Try to increase the day, if it is invalid, an OSError is thrown, then reset day to 0
        try:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_MINUTE] = current_datetime[constants.RTC_MINUTE] + 1
            self.rtc.datetime(tuple(current_datetime_list))
        except OSError:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_MINUTE] = 0
            self.rtc.datetime(tuple(current_datetime_list))
            
    def decrement_minute(self):
        """Decrement minute counter in rtc"""
        current_datetime = self.rtc.datetime()
        # Try to increase the day, if it is invalid, an OSError is thrown, then reset day to 0
        try:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_MINUTE] = current_datetime[constants.RTC_MINUTE] - 1
            self.rtc.datetime(tuple(current_datetime_list))
        except OSError:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_MINUTE] = 59
            self.rtc.datetime(tuple(current_datetime_list))

    def decrement_hour(self):
        """Decrements the hour counter in the rtc"""
        current_datetime = self.rtc.datetime()
        # Try to increase the day, if it is invalid, an OSError is thrown, then reset day to 0
        try:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_HOUR] = current_datetime[constants.RTC_HOUR] - 1
            self.rtc.datetime(tuple(current_datetime_list))
        except OSError:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_HOUR] = 23
            self.rtc.datetime(tuple(current_datetime_list))


    def decrement_year(self):
        """Decrements the year counter in the rtc"""
        current_datetime = self.rtc.datetime()
        # Try to increase the year, if it is invalid, an OSError is thrown, then reset year to 0
        try:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_YEAR] = current_datetime[constants.RTC_YEAR] - 1
            self.rtc.datetime(tuple(current_datetime_list))
        except OSError:
            current_datetime_list = list(current_datetime)
            current_datetime_list[constants.RTC_YEAR] = 2000
            self.rtc.datetime(tuple(current_datetime_list))
        
    def decrement_month(self):
        """Decrements the month counter in the rtc, with valid decrement correction"""
        current_datetime = self.rtc.datetime()
        current_datetime_list = list(current_datetime)

        # Adjust Month
        if current_datetime_list[constants.RTC_MONTH] - 1 <= 0:
            current_datetime_list[constants.RTC_MONTH] = 12
        else:
            current_datetime_list[constants.RTC_MONTH] = current_datetime_list[constants.RTC_MONTH] - 1
        # Adjust day if necessary, ensuring the days match up if leap year    
        if check_leap_year(current_datetime_list[constants.RTC_YEAR]):
            real_days_in_month = constants.days_in_month_leap[current_datetime_list[constants.RTC_MONTH]]             
        else:
            real_days_in_month = constants.days_in_month[current_datetime_list[constants.RTC_MONTH]]
        
        if current_datetime_list[constants.RTC_DAY] > real_days_in_month:
            # Update the day
            current_datetime_list[constants.RTC_DAY] = real_days_in_month 

        #Update the time                                                                                                                                 
        self.rtc.datetime(tuple(current_datetime_list))

        
    def decrement_day(self):
        """Decrements the day counter in the rtc, with valid day correction"""
        current_datetime = self.rtc.datetime()
        current_datetime_list = list(current_datetime)

        # Check for leap year
        if check_leap_year(current_datetime_list[constants.RTC_YEAR]):
            real_days_in_month = constants.days_in_month_leap[current_datetime_list[constants.RTC_MONTH]]             
        else:
            real_days_in_month = constants.days_in_month[current_datetime_list[constants.RTC_MONTH]]
        
        # Adjust day
        if current_datetime_list[constants.RTC_DAY] - 1 <= 0 :
            current_datetime_list[constants.RTC_DAY] = real_days_in_month
        else:
            current_datetime_list[constants.RTC_DAY] = current_datetime_list[constants.RTC_DAY] - 1
        
        # Update the time
        self.rtc.datetime(tuple(current_datetime_list))
