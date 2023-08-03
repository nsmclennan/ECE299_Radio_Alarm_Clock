"""
*    Title: Button Management for Radio Alarm Clock
*    Author: Nicholas McLennan
*    Date: July 20, 2023
*    Code version: 1.0
"""

import constants
import utime


def update_display_state(button_number, display, clock, fm_radio_module, alarm_output):
    """Update the current display state based on the button 
       input detected and current state

    Args:
        button_number (int): button number that got inputted
        display (Display): Display object that contains the display information
        clock (Clock): Clock object that contains clock/alarm info
        fm_radio_module (Radio): Radio object that contains the radio information
        alarm_output (PWM): PWM object that contains the alarm output pin
    """
    
    
    # Pick which button was pressed
    if button_number == 1:
        # Depending on the current state, complete the functionality of the button
        if display.state == constants.DEFAULT_CLOCK:
            display.state = constants.MAIN_MENU
            display.settings_start_index = 0
            display.settings_active_index = 0
        
        elif display.state == constants.MAIN_MENU:
            display.decrement_active_index()

        elif display.state == constants.BRIGHTNESS_MENU:
            display.increment_brightness()

        elif display.state == constants.VOLUME_MENU:
            fm_radio_module.IncrementVolume()

        elif display.state == constants.CHANGE_FM_STATION_MENU:
            fm_radio_module.ModifyStation(0.2)

        elif display.state == constants.ALARM_OFF:
            # Return to previous radio state before alarm
            if fm_radio_module.radio_module_previously_on is True:
                fm_radio_module.SetMute(False)
                fm_radio_module.ProgramRadio()
                fm_radio_module.radio_module_previously_on = False
            # Reset State
            display.state = constants.DEFAULT_CLOCK
            # Ensure audio is off
            alarm_output.duty_u16(0)
            # Reset snooze
            clock.alarm_triggered = False

        elif display.state == constants.ADJUST_DATE_MENU:
            state = display.selected_date_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_YEAR:
                clock.increment_year()
            elif state == constants.SET_MONTH:
                clock.increment_month()
            elif state == constants.SET_DAY:
                clock.increment_day()
                
        elif display.state == constants.ADJUST_TIME_MENU:
            state = display.selected_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.increment_hour()
            elif state == constants.SET_MINUTE:
                clock.increment_minute()
            elif state == constants.SET_FORMAT:
                display.toggle_hour_format()
                
        elif display.state == constants.SET_ALARM_1_WEEKDAY:
            state = display.selected_alarm_weekday_index
            # If the user is updating a weekday
            if state != constants.WEEKDAY_CONFIRM:
                clock.alarms[0].add_weekday(display.selected_alarm_weekday_index)
            # Otherwise, ignore user input
                
        
        elif display.state == constants.SET_ALARM_2_TIME:
            state = display.selected_alarm_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.alarms[1].increment_hour()
            elif state == constants.SET_MINUTE:
                clock.alarms[1].increment_minute()

        elif display.state == constants.SET_ALARM_2_WEEKDAY:
            state = display.selected_alarm_weekday_index
            # If the user is updating a weekday
            if state != constants.WEEKDAY_CONFIRM:
                clock.alarms[1].add_weekday(display.selected_alarm_weekday_index)
            # Otherwise, ignore user input
                
        
        elif display.state == constants.SET_ALARM_3_TIME:
            state = display.selected_alarm_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.alarms[2].increment_hour()
            elif state == constants.SET_MINUTE:
                clock.alarms[2].increment_minute()

        elif display.state == constants.SET_ALARM_3_WEEKDAY:
            state = display.selected_alarm_weekday_index
            # If the user is updating a weekday
            if state != constants.WEEKDAY_CONFIRM:
                clock.alarms[2].add_weekday(display.selected_alarm_weekday_index)
            # Otherwise, ignore user input
                
        
        elif display.state == constants.SET_ALARM_1_TIME:
            state = display.selected_alarm_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.alarms[0].increment_hour()
            elif state == constants.SET_MINUTE:
                clock.alarms[0].increment_minute()
           
        elif display.state == constants.DELETE_ALARMS:
            state = display.selected_deleted_alarm_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.ALARM_1:
                clock.alarms[0].toggle_user_enable()
            elif state == constants.ALARM_2:
                clock.alarms[1].toggle_user_enable()
            elif state == constants.ALARM_3:
                 clock.alarms[2].toggle_user_enable()

    elif button_number == 2:
        # Depending on the current state, complete the functionality of the button
        if display.state == constants.DEFAULT_CLOCK:
            display.state = constants.MAIN_MENU
            display.settings_start_index = 0
            display.settings_active_index = 0

        elif display.state == constants.MAIN_MENU:
            display.increment_active_index()

        elif display.state == constants.BRIGHTNESS_MENU:
            display.decrement_brightness()

        elif display.state == constants.VOLUME_MENU:
            fm_radio_module.DecrementVolume()

        elif display.state == constants.CHANGE_FM_STATION_MENU:
            fm_radio_module.ModifyStation(-0.2)

        elif display.state == constants.ALARM_OFF:
            # Return to previous radio state before alarm
            if fm_radio_module.radio_module_previously_on is True:
                fm_radio_module.SetMute(False)
                fm_radio_module.ProgramRadio()
                fm_radio_module.radio_module_previously_on = False
            # Reset State
            display.state = constants.DEFAULT_CLOCK
            # Ensure audio is off
            alarm_output.duty_u16(0)
            # Reset snooze
            clock.alarm_triggered = False

        elif display.state == constants.ADJUST_DATE_MENU:
            state = display.selected_date_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_YEAR:
                clock.decrement_year()
            elif state == constants.SET_MONTH:
                clock.decrement_month()
            elif state == constants.SET_DAY:
                clock.decrement_day()
                
        elif display.state == constants.ADJUST_TIME_MENU:
            state = display.selected_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.decrement_hour()
            elif state == constants.SET_MINUTE:
                clock.decrement_minute()
            elif state == constants.SET_FORMAT:
                display.toggle_hour_format()
                
        elif display.state == constants.SET_ALARM_1_WEEKDAY:
            state = display.selected_alarm_weekday_index
            # If the user is updating a weekday
            if state != constants.WEEKDAY_CONFIRM:
                clock.alarms[0].remove_weekday(display.selected_alarm_weekday_index)
            # Otherwise, ignore user input

        # Remove
        elif display.state == constants.SET_ALARM_1_TIME:
            state = display.selected_alarm_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.alarms[0].decrement_hour()
            elif state == constants.SET_MINUTE:
                clock.alarms[0].decrement_minute()

        elif display.state == constants.SET_ALARM_2_WEEKDAY:
            state = display.selected_alarm_weekday_index
            # If the user is updating a weekday
            if state != constants.WEEKDAY_CONFIRM:
                clock.alarms[1].remove_weekday(display.selected_alarm_weekday_index)
            # Otherwise, ignore user input

        elif display.state == constants.SET_ALARM_2_TIME:
            state = display.selected_alarm_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.alarms[1].decrement_hour()
            elif state == constants.SET_MINUTE:
                clock.alarms[1].decrement_minute()

        elif display.state == constants.SET_ALARM_3_WEEKDAY:
            state = display.selected_alarm_weekday_index
            # If the user is updating a weekday
            if state != constants.WEEKDAY_CONFIRM:
                clock.alarms[2].remove_weekday(display.selected_alarm_weekday_index)
            # Otherwise, ignore user input

        elif display.state == constants.SET_ALARM_3_TIME:
            state = display.selected_alarm_time_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.SET_HOUR:
                clock.alarms[2].decrement_hour()
            elif state == constants.SET_MINUTE:
                clock.alarms[2].decrement_minute()
                
        elif display.state == constants.DELETE_ALARMS:
            state = display.selected_deleted_alarm_index
            # Depending on the current state of the menu,
            # change different parameters
            if state == constants.ALARM_1:
                clock.alarms[0].toggle_initialize()
            elif state == constants.ALARM_2:
                clock.alarms[1].toggle_initialize()
            elif state == constants.ALARM_3:
                clock.alarms[2].toggle_initialize()
            
                
            

    elif button_number == 3:
        # Depending on the current state, complete the functionality of the button.
        if display.state == constants.DEFAULT_CLOCK:
            display.state = constants.MAIN_MENU
            display.settings_start_index = 0
            display.settings_active_index = 0

        elif display.state == constants.MAIN_MENU:
            display.state = constants.setting_state_list[display.settings_active_index]
            # Reset time change parameters if entering state
            if constants.setting_state_list[display.settings_active_index] == constants.ADJUST_TIME_MENU:
                display.selected_time_index = 0
            elif constants.setting_state_list[display.settings_active_index] == constants.ADJUST_DATE_MENU:
                display.selected_date_index = 0
            elif constants.setting_state_list[display.settings_active_index] == constants.SET_ALARM_1_WEEKDAY:
                display.selected_alarm_weekday_index = 0
                display.selected_alarm_time_index = 0
            elif constants.setting_state_list[display.settings_active_index] == constants.SET_ALARM_2_WEEKDAY:
                display.selected_alarm_weekday_index = 0
                display.selected_alarm_time_index = 0
            elif constants.setting_state_list[display.settings_active_index] == constants.SET_ALARM_3_WEEKDAY:
                display.selected_alarm_weekday_index = 0
                display.selected_alarm_time_index = 0
            elif constants.setting_state_list[display.settings_active_index] == constants.DELETE_ALARMS:
                display.selected_deleted_alarm_index = 0
                
        elif display.state == constants.CHANGE_FM_STATION_MENU:
            fm_radio_module.ToggleMute()
        
        elif display.state == constants.ALARM_OFF:
            # Return to previous radio state before alarm
            if fm_radio_module.radio_module_previously_on is True:
                fm_radio_module.SetMute(False)
                fm_radio_module.ProgramRadio()
                fm_radio_module.radio_module_previously_on = False
            # Reset State
            display.state = constants.DEFAULT_CLOCK
            # Ensure audio is off
            alarm_output.duty_u16(0)
            # Reset snooze
            clock.alarm_triggered = False

        elif display.state == constants.ADJUST_TIME_MENU:
            display.selected_time_index += 1
            if display.selected_time_index >= constants.LENGTH_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU

        elif display.state == constants.ADJUST_DATE_MENU:
            display.selected_date_index += 1
            if display.selected_date_index >= constants.LENGTH_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU
                
                
        elif display.state == constants.SET_ALARM_1_WEEKDAY:
            display.selected_alarm_weekday_index += 1
            if display.selected_alarm_weekday_index >= constants.LENGTH_OF_WEEKDAY_MENU_LIST:
                display.state = constants.SET_ALARM_1_TIME
                
        elif display.state == constants.SET_ALARM_1_TIME:
            display.selected_alarm_time_index += 1
            if display.selected_alarm_time_index >= 3:
                clock.alarms[0].initialized = True
                clock.alarms[0].user_enabled = True
                display.state = constants.MAIN_MENU

        elif display.state == constants.SET_ALARM_2_WEEKDAY:
            display.selected_alarm_weekday_index += 1
            if display.selected_alarm_weekday_index >= constants.LENGTH_OF_WEEKDAY_MENU_LIST:
                display.state = constants.SET_ALARM_2_TIME
                
        elif display.state == constants.SET_ALARM_2_TIME:
            display.selected_alarm_time_index += 1
            if display.selected_alarm_time_index >= 3:
                clock.alarms[1].initialized = True
                clock.alarms[1].user_enabled = True
                display.state = constants.MAIN_MENU
                
        elif display.state == constants.SET_ALARM_3_WEEKDAY:
            display.selected_alarm_weekday_index += 1
            if display.selected_alarm_weekday_index >= constants.LENGTH_OF_WEEKDAY_MENU_LIST:
                display.state = constants.SET_ALARM_3_TIME
                
        elif display.state == constants.SET_ALARM_3_TIME:
            display.selected_alarm_time_index += 1
            if display.selected_alarm_time_index >= 3:
                clock.alarms[2].initialized = True
                clock.alarms[2].user_enabled = True
                display.state = constants.MAIN_MENU

        elif display.state == constants.DELETE_ALARMS:
            display.selected_deleted_alarm_index += 1
            if display.selected_deleted_alarm_index >= constants.LENGTH_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU

    elif button_number == 4:
        # Depending on the current state, complete the functionality of the button.
        # Main functionality is as a back button
        if display.state == constants.DEFAULT_CLOCK:
            display.state = constants.MAIN_MENU
            display.settings_start_index = 0
            display.settings_active_index = 0

        elif display.state == constants.MAIN_MENU:
            display.state = constants.DEFAULT_CLOCK

        elif display.state == constants.BRIGHTNESS_MENU:
            display.state = constants.MAIN_MENU

        elif display.state == constants.VOLUME_MENU:
            display.state = constants.MAIN_MENU

        elif display.state == constants.ALARM_OFF:
            # Return to previous radio state before alarm
            if fm_radio_module.radio_module_previously_on is True:
                fm_radio_module.SetMute(False)
                fm_radio_module.ProgramRadio()
                fm_radio_module.radio_module_previously_on = False
            # Reset State
            display.state = constants.DEFAULT_CLOCK
            # Ensure audio is off
            alarm_output.duty_u16(0)
            # Reset snooze
            clock.alarm_triggered = False

        elif display.state == constants.ADJUST_DATE_MENU:
            display.selected_date_index -= 1
            if display.selected_date_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU

        elif display.state == constants.CHANGE_FM_STATION_MENU:
            display.state = constants.MAIN_MENU

        elif display.state == constants.ADJUST_TIME_MENU:
            display.selected_time_index -= 1
            if display.selected_time_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU
                
        elif display.state == constants.SET_ALARM_1_WEEKDAY:
            display.selected_alarm_weekday_index -= 1
            if display.selected_alarm_weekday_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU

        elif display.state == constants.SET_ALARM_1_TIME:
            display.selected_alarm_time_index -= 1
            if display.selected_alarm_time_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.SET_ALARM_1_WEEKDAY
                display.selected_alarm_time_index = 0
                display.selected_alarm_weekday_index = 0

        elif display.state == constants.SET_ALARM_2_WEEKDAY:
            display.selected_alarm_weekday_index -= 1
            if display.selected_alarm_weekday_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU

        elif display.state == constants.SET_ALARM_2_TIME:
            display.selected_alarm_time_index -= 1
            if display.selected_alarm_time_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.SET_ALARM_2_WEEKDAY
                display.selected_alarm_time_index = 0
                display.selected_alarm_weekday_index = 0
                
        elif display.state == constants.SET_ALARM_3_WEEKDAY:
            display.selected_alarm_weekday_index -= 1
            if display.selected_alarm_weekday_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.MAIN_MENU

        elif display.state == constants.SET_ALARM_3_TIME:
            display.selected_alarm_time_index -= 1
            if display.selected_alarm_time_index < constants.START_OF_SETTINGS_LIST:
                display.state = constants.SET_ALARM_3_WEEKDAY
                display.selected_alarm_time_index = 0
                display.selected_alarm_weekday_index = 0

        elif display.state == constants.DELETE_ALARMS:
            display.selected_deleted_alarm_index -= 1
            if display.selected_deleted_alarm_index < 0:
                display.state = constants.MAIN_MENU
        



