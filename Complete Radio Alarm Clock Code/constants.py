"""Module that contains constants for main function code"""

"""
*    Title: Constants for Radio Alarm Clock
*    Author: Nicholas McLennan
*    Date: July 20, 2023
*    Code version: 1.0
"""

# Frequencies for PWM alarm
pulse_freq = [
    500,
    500,
    500,
    250,
    250,
    250,
    750,
    750,
    750,
    1000,
    1000,
    1000,
]

pulse_duty = [
    256,
    512,
    867,
    256,
    512,
    867,
    256,
    512,
    867,
    256,
    512,
    867,
]

MAX_NUM_ALARM_NOTES = 12

# To wrap decrement day to the largest day in the month
days_in_month = [
    00, # Filler so indexing starts at 1
    31,
    28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
    ]

days_in_month_leap = [
    00, # Filler so indexing starts at 1
    31,
    29,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
    ]

# Constants for statemachine states
(
# Main States
DEFAULT_CLOCK,
MAIN_MENU,

# Date and Time Menu States
ADJUST_TIME_MENU,
ADJUST_DATE_MENU,

# Alarms and Radio Menu States
CHANGE_FM_STATION_MENU,

# Settings Menu States
BRIGHTNESS_MENU,
VOLUME_MENU,

# Alarm States
ALARM_OFF,
DELETE_ALARMS,
SET_ALARM_1_WEEKDAY,
SET_ALARM_1_TIME,
SET_ALARM_2_WEEKDAY,
SET_ALARM_2_TIME,
SET_ALARM_3_WEEKDAY,
SET_ALARM_3_TIME,

)= range(0,15)

# Bounds for menu settings
LENGTH_OF_SETTINGS_LIST = 4
START_OF_SETTINGS_LIST = 0

#Alarm Constants

(
 MONDAY,
 TUESDAY,
 WEDNESDAY,
 THURSDAY,
 FRIDAY,
 SATURDAY,
 SUNDAY,
 )= range(0,7)
 
days = [
    "M",
    "T",
    "W",
    "R",
    "F",
    "S",
    "U",
    ]
months = [
    "NAN",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    ]

# Setting states
setting_state_list = [
    CHANGE_FM_STATION_MENU,
    VOLUME_MENU,
    SET_ALARM_1_WEEKDAY,
    SET_ALARM_2_WEEKDAY,
    SET_ALARM_3_WEEKDAY,
    DELETE_ALARMS,
    ADJUST_TIME_MENU,
    ADJUST_DATE_MENU,
    BRIGHTNESS_MENU,
    ]
# For Display
full_list = [
    "Radio FM",
    "Volume",
    "Alarm 1",
    "Alarm 2",
    "Alarm 3",
    "Delete Alarms",
    "Set Time",
    "Set Date",
    "Brightness",
    ]
MAX_NUM_SETTINGS = 8

# For Setting Time Menu
selected = ["Hour", "Minute"]



#Set Time Display States
(
    SET_HOUR,
    SET_MINUTE,
    SET_FORMAT,
    CONFIRM
)= range(0,4)

# Set Date Display States
(
    SET_YEAR,
    SET_MONTH,
    SET_DAY,
    CONFIRM
) = range(0,4)
    
# Set Alarm Weekday Display States
(
    SET_MONDAY,
    SET_TUESDAY,
    SET_WEDNESDAY,
    SET_THURSDAY,
    SET_FRIDAY,
    SET_SATURDAY,
    SET_SUNDAY,
    WEEKDAY_CONFIRM
) = range (0, 8)
LENGTH_OF_WEEKDAY_MENU_LIST = 8

# Set Alarm Time Display States
(
    SET_HOUR,
    SET_MINUTE,
    TIME_CONFIRM
) = range (0,3)

# Delete Alarm Display States
(
    ALARM_1,
    ALARM_2,
    ALARM_3,
    CONFIRM
) = range (0,4) 

#Constants for RTC to index
(
RTC_YEAR,
RTC_MONTH,
RTC_DAY,
RTC_WEEKDAY,
RTC_HOUR,
RTC_MINUTE,
RTC_SECOND,
RTC_SUB_SECOND,
) = range(0,8)

# For positioning object sin setting alarm screen
set_alarm_height_row1 = 0
set_alarm_height_row2 = 20
set_alarm_height_row3 = 35
set_alarm_height_row4 = set_alarm_height_row3+4

# For building new alarms
empty_alarm_weekdays_1 = [False] * 7
empty_alarm_weekdays_2 = [False] * 7
empty_alarm_weekdays_3 = [False] * 7
