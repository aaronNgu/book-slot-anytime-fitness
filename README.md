## What's this script for?
This script is used to book a slot from https://reserve.anytimefitness.com/. 
The script books a time slot two days from the day the script runs. 
For example, if I run the script on Monday morning,
it will book a time slot(that I specify in the config.json) for Wednesday.
This is so that I can book the time slot right when it is made available to the public. 

## Prerequisite 
Install python3 

##How to use the script?
1. Create file `config.json` at the same location as where you want to run the script.
2. Inside copy and paste the contents of `config.json.sample` into `config.json`
3. Modify the contents of the `config.json` accordingly. 
    `club` value should be "3226" for the anytime fitness at Burnaby Metrotown.
    `keyfob` value can be found on your keyfob.
    `times` are "day":"time" values, where "time" is in 24 hour time format
    and "day" is the day you want to go to the gym. i.e. "1" - Monday "3" - Wednesday.
4.  Run the script with `python3 book-slot.py`.

## How to automate the script?(Mac) 
1. Create a python virtual env `python3 env` 
    at the same location as where you want to run the script.
2. Move `com.anytime.fitness.plist` to `~/Library/LaunchAgents`
3. Inside `~/Library/LaunchAgents/com.anytime.fitness.plist` 
    specify the day and time to run the script after `<key>StartCalendarInterval</key>`.
4. Make sure your machine(laptop) is not asleep at the time the script is suppose to run. 
    [instructions here](https://support.apple.com/en-ca/guide/mac-help/mchlp2266/mac#:~:text=On%20your%20Mac%2C%20choose%20Apple,Preferences%2C%20then%20click%20Energy%20Saver.&text=Click%20Schedule%20in%20the%20bottom,Start%20up%20or%20wake%E2%80%9D%20checkbox.)

Note: make sure you run your script two days before the day you actually want to go to the gym.
If you want to book a slot for Friday, 
you need to run this script on Wednesday
(preferably early in the morning at 00:10) to make sure the slots are not all booked up.
