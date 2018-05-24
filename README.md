# pi-alarm-clock

This creates alarms by automatically scheduling cron jobs that run an alarm script at different times. Once the alarm is playing, is can be disabled by pressing a physical button, and is currently set to use GPIO pin 4. Use addalarm.py to add alarms and delalarm.py to delete alarms. The location of the alarm script and the directory of alarm sounds are set by the files ~/.alarm-location and ~/.alarms-location, respectively. 

## Dependencies

### System
- cron

### Python
3.4 or greater
gpiozero

