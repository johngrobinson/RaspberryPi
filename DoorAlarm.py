#!/usr/bin/python

# Imports the sys module provides a number of functions and variables that can    #
# be used to manipulate different parts of the Python runtime environment.        #
import sys
import threading
from threading import Thread
# Imports signal module that set handlers for asynchronous events                 #
import signal
# Imports time to use for the pauses or sleep in the code                         #
import time
from time import gmtime, strftime, localtime
# Import smtplib to provide email functions
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
global emailCount

# Imports the Raspberry Pi GPIO library and sets RPi.GPIO to GPIO                 #
import RPi.GPIO as io

# Sets GPIO to where you can refer to the pins by the "Broadcom SOC channel"      #
# number, these are the numbers after "GPIO"                                      #
io.setmode(io.BCM)
io.setwarnings(False)


####################### SIGNAL HANDLER TO CATCH CTRL+C   ##########################
# Setup signal handler to catch ctrl+c detectGPIOn and exit cleanly               #
###################################################################################
def signal_handler(signal, frame):
    print("Ctrl+C detected...")
    io.cleanup()
    sys.exit(0)


# set signal handler                                                              #
signal.signal(signal.SIGINT, signal_handler)
#                                                                                 #
####################### SIGNAL HANDLER TO CATCH CTRL+C END ########################

####################### CURRENT DATE AND TIME STAMP      ##########################
# This function provides a simple date and time stamp. Just call                  #
# door_timestamp(0). EXAMPLE: print(door_timestamp(0)- Sat, 27 Feb 2016 18:21:37  #
###################################################################################
def door_timestamp(sec=0):
    if sec == 0:
        sec = time.time()
    return strftime("%a, %d %b %Y %H:%M:%S ", time.localtime(sec))



#                                                                                 #
####################### CURRENT DATE AND TIME STAMP END    ########################




####################### LED_PIN CREATION SECTION START  ###########################
# Here is where you set the GPIO pin for the led and pin the output to the GPIO   #
###################################################################################

# Sets the led GPIO to pin 21                                                     #
led_pin = 21
# Setup GPIO Pin 21 to OUT                                                        #
io.setup(led_pin, io.OUT)
# Turn on GPIO pin 21                                                             #
io.output(led_pin, False)
#                                                                                 #
####################### LED_PIN CREATION SECTION END  #############################


####################### DOOR SENSOR CREATION SECTION START  #######################
# Here is where you set up the GPIO pin for the door sensor and sets the          #
# GPIO output.                                                                    #
###################################################################################

# this sets the GPIO pin to 26
door_pin = 26
# activate input with PullUp for the door sensor
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)
CurrentState = io.input(door_pin)


#                                                                                 #
####################### DOOR SENSOR CREATION SECTION END  #########################





####################### EMAIL CREATION SECTION START ##############################
# This code is used to email out a notification if the magnetic door sensor has   #
# been triggered.                                                                 #
# Begin mail setup, this code is written for GMAIL but you could easily re-write  #
# the current code by changing the GMAIL setup properties with Hotmail or what    #
# ever smtp mail service.                                                         #
###################################################################################
count = 1


def emailalert():
    # how may times you get emailed. This will loop twice and send the email out.
    print(io.input(door_pin), " - Email Being Sent")
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.

    server.sendmail(me, you, msg.as_string())
    if (io.input(door_pin) == io.LOW):
        time.sleep(30)
    server.quit()


####################### BLINK FUNCTION CREATION SECTION START  ####################
# Defines a function called Blink. This function will light up an LED             #
# when the door is opened.                                                        #
###################################################################################



# This is where we set the Blink function and set all the variables on how fast
# or how often the led light blinks
iterations = 20
speed1 = 10
numTimes = 10


def blink(numTimes, speed1):
    for i in range(0, 10):  # Run loop numTimes
        io.output(led_pin, True)  # Switch on led_pin
        time.sleep(1)  # Wait
        io.output(led_pin, False)  # Switch off led_pint
        # return blink(10, speed1)


####################### BLINK FUNCTION CREATION SECTION END  ######################









####################### DOOR SENSOR CREATION SECTION END  #####################

####################### MAIN CODE CREATION SECTION START  #####################
#######################                                   #####################
####################### CODE THAT RUNS THE CHECK ON IS    #####################
####################### THE DOOR OPEN AND HAVE I EMAILED  #####################
####################### THE ALERT AND FLASHED THE LED     #####################




try:

    print("Waiting for Door Sensor to settle ...", io.input(door_pin))

    # Loop until PIR output is 0
    # while io.input(door_pin) == io.HIGH:


    # loop until CurrentState = 1 or user quits with ctrl-c

    while True:
        # Loop through the CurrentState of the door sensor and Previous States #
        if io.input(door_pin) == io.HIGH:
            print(io.input(door_pin))
        elif io.input(door_pin) == io.LOW:

            me = 'johngrobinson@gmail.com'
            you = "jrotton@hotmail.com; johngrobinson@hotmail.com"

            # GMAIL user setup #
            gmail_sender = 'johngrobinson@gmail.com'
            gmail_passwd = 'Monkeybutt2'
            subject = 'FRONT DOOR HAS HAS OPENED at ' + door_timestamp(0)

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = me
            msg['To'] = you
            hbody = '<html><head></head><body><p> ' + subject + '<br><br>Do you know where you daughter is?<br><br>At ' + door_timestamp(
                0) + ' your front door was opened.</p></body></html>'

            # Create the body of the message (a plain-text and an HTML version).
            text = subject + "!\nDo you know where you daughter is?\n"
            html = hbody

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)

            # Send the message via gmail SMTP server.
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.set_debuglevel(0)
            server.ehlo(gmail_sender)
            server.starttls()
            server.ehlo(gmail_sender)
            server.login(gmail_sender, gmail_passwd)

            if __name__ == '__main__':
                Thread(target=emailalert()).start()
                Thread(target=blink(numTimes, speed1)).start()



    time.sleep(15)


####################### MAIN CODE CREATION SECTION END     #####################


####################### CODE CLEAN UP CREATION SECTION     #####################

except KeyboardInterrupt:
    print("Quit")
    # Reset GPIO settings
    io.cleanup()

####################### CODE CLEAN UP CREATION SECTION END  #####################
