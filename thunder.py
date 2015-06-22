#!/usr/bin/python
##########################################################################################
# 
# Thunder War - an office warefare action starter
#
#    Make them pay for build failures, and sometimes for just being in the room :)
#
# Steps to use:
#
#  1.  Mount your Dream Cheeky Thunder USB missile launcher in a central and 
#      fixed location.
#
#  2.  Copy this script onto the system connected to your missile lanucher.
#
#  3.  Modify `USERS_COMMANDS_SEQUENCES` map variable to define your targeting commands
#      for each one of your build-breaking coders (their user ID as listed in Jenkins).
#      A command set is an array of move and fire commands.
#      It is recommend to start each command set with a "zero" command.
#      This parks the launcher in a known position (bottom-left).
#      You can then use "up" and "right" followed by a 
#      time (in milliseconds) to position your fire.
# 
#      You can test or manually shoot someone by calling thunder-war.py with the target name. 
#      e.g.:  
#
#           thunder-war.py "[developer's user name]"
#
#      Trial and error is the best approch. Consider doing this secretly 
#      after hours for best results!
#
#  4.  Setup the Jenkins "notification" plugin. Define a UDP endpoint 
#      on port 6666 pointing to the system hosting this script.
#      Tip: Make sure your firewall is not blocking UDP on this port.
#
#  5.  Start listening for failed build events by running the command:
#          retaliation.py stalk
#      (Consider setting this up as a boot/startup script. On Windows 
#      start with pythonw.exe to keep it running hidden in the 
#      background.)
#
#  Requirements & installation notes can be found in README.txt
#
#  Author:  Sahar <koryoislie@gmail.com> (based on Chris Dance retailiation script. Chris --> You`re awesome!)
#  Version: 1.0 : 01/04/2015
#
##########################################################################################

import sys
import platform
import time
import socket
import re
import json
import urllib2
import base64

import usb.core
import usb.util

import winsound
import threading
import thread
import random
import datetime

##########################  CONFIG   #########################

#
# Define a dictionary of "command sets" that map usernames to a sequence 
# of commands to target the user (e.g their desk/workstation).  It's 
# suggested that each set start and end with a "zero" command so it's
# always parked in a known reference location. The timing on move commands
# is milli-seconds. The number after "fire" denotes the number of rockets
# to shoot.
#
USERS_COMMANDS_SEQUENCES = {
    "daniel.elkayam" : (
        ("zero", 0), # Zero/Park to know point (bottom-left)
        ("led", 1), # Turn the LED on
        ("right", 600),
        ("up", 500),
        ("fire", 2), # Fire a barrage of 2 missiles
        ("led", 0), # Turn the LED back off
        ("zero", 0), # Park after use for next time
    ),
    "yosef" : (
        ("zero", 0),
        ("up", 500),
        ("right", 1650),
        ("fire", 1),
        ("fire", 2),
        ("zero", 0),
    ),
    "boris" : (      
        ("zero", 0),
        ("right", 700),
        ("up", 550),
        ("fire", 1),
        ("zero", 0),
    ),
    "assafa" : (
        ("zero", 0), 
        ("right", 300),
        ("up", 400),
        ("fire", 1),
        ("zero", 0),
    ),
    "saharh" : (     # That's me - just dance around and don`t shoot of course
        ("zero", 0),
        ("right", 3300),
        ("up", 600),
        ("pause", 1000),
        ("fire", 1),
        ("up", 100),
        ("zero", 0),
    ),
    "gal.omershimoni" : (       #although she`s in a different room, we would like to know when she breaks the wall
        ("zero", 0), 
        ("right", 4500),
        ("up", 1000),
        ("fire", 1),
        ("zero", 0),
    ),
}

#
# The UDP port to listen to Jenkins events on (events are generated/supplied 
# by Jenkins "notification" plugin)
#
JENKINS_NOTIFICATION_UDP_PORT   = 6666

#
# The URL of your Jenkins server - used to callback to determine who broke 
# the build.
#
JENKINS_SERVER                  = "http://10.0.0.29"

#
# If you're Jenkins server is secured by HTTP basic auth, sent the
# username and password here.  Else leave this blank.
HTTPAUTH_USER                   = ""
HTTPAUTH_PASS                   = ""

##########################  END CONFIG  #########################

# The code...

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None
DEVICE_TYPE = None

SLEEP_DURATION = 4

# call this function if you want to make things more interesting instead of counting of your friends` poor programming skills
FIRST_SHOT = True
def shoot_once_a_while():
    global FIRST_SHOT 
    # if this is the first shot - don`t shoot, just set a timer
    if (not FIRST_SHOT):
        #choose *randomly* who to shoot
        random_user = random.sample(USERS_COMMANDS_SEQUENCES.items(), 1)[0][0]
        print "Chosen user is %s" %(random_user)

        # SHOOT IT!
        jenkins_target_user(random_user)
    else:
        FIRST_SHOT = False
    
    # choose next shot at random time 
    MINIMUM_WORKING_HOURS = datetime.time(9,30)
    MAXIMUM_WORKING_HOURS = datetime.time(18,30)

    # once between 3 to 6 hours, in minutes
    min_to_next_run = random.randint(120,240)
    
    target_datetime = (datetime.datetime.now() + datetime.timedelta(minutes = min_to_next_run))
    target_time = datetime.time(target_datetime.hour, target_datetime.minute)

    # make sure time in working hours
    if target_time >= MINIMUM_WORKING_HOURS and target_time <= MAXIMUM_WORKING_HOURS :
        print "\n* Next random shooting time is within working hours... Be carefull, especially at %s :>" %(str(target_time))
        target_datetime = datetime.datetime.combine(datetime.datetime.now(), target_time)
        threading.Timer((target_datetime - datetime.datetime.now()).total_seconds(), shoot_once_a_while).start()
    else:
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        target_time = datetime.datetime.combine(tomorrow, MINIMUM_WORKING_HOURS) + datetime.timedelta(minutes = min_to_next_run)
        print "\n* Next random shooting time is not within working hours. Cya tomorrow at %s" %(str(target_time))
        threading.Timer((target_time - datetime.datetime.now()).total_seconds(), shoot_once_a_while).start()

def play_sound(path, *args):
    winsound.PlaySound(path, winsound.SND_FILENAME)

def usage():
    print "Usage: retaliation.py [command] [value]"
    print ""
    print "   commands:"
    print "     stalk - sit around waiting for a Jenkins CI failed build"
    print "             notification, then attack the perpetrator!"
    print ""
    print "     up    - move up <value> milliseconds"
    print "     down  - move down <value> milliseconds"
    print "     right - move right <value> milliseconds"
    print "     left  - move left <value> milliseconds"
    print "     fire  - fire <value> times (between 1-4)"
    print "     zero  - park at zero position (bottom-left)"
    print "     pause - pause <value> milliseconds"
    print "     led   - turn the led on or of (1 or 0)"
    print ""
    print "     <command_set_name> - run/test a defined COMMAND_SET"
    print "             e.g. run:"
    print "                  retaliation.py 'sahar'"
    print "             to test targeting of sahar as defined in your command set."
    print ""


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    # and original USB Launcher
    global DEVICE 
    global DEVICE_TYPE

    # find Thunder Cheeky USB device
    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
        if DEVICE is None:
            raise ValueError('Missile device not found')
        else:
            DEVICE_TYPE = "Original"
    else:
        DEVICE_TYPE = "Thunder"

    

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()


def send_cmd(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0x0200, 0, [cmd])

def led(cmd):
    if "Thunder" == DEVICE_TYPE:
        DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
    elif "Original" == DEVICE_TYPE:
        print("There is no LED on this device")

def send_move(cmd, duration_ms):
    send_cmd(cmd)
    time.sleep(duration_ms / 1000.0)
    send_cmd(STOP)


def run_command(command, value):
    command = command.lower()
    if command == "right":
        send_move(RIGHT, value)
    elif command == "left":
        send_move(LEFT, value)
    elif command == "up":
        send_move(UP, value)
    elif command == "down":
        send_move(DOWN, value)
    elif command == "zero" or command == "park" or command == "reset":
        # Move to bottom-left
        send_move(DOWN, 2000)
        send_move(LEFT, 8000)
    elif command == "pause" or command == "sleep":
        time.sleep(value / 1000.0)
    elif command == "led":
        if value == 0:
            led(0x00)
        else:
            led(0x01)
    elif command == "fire" or command == "shoot":
        if value < 1 or value > 4:
            value = 1
        # Stabilize prior to the shot, then allow for reload time after.
        time.sleep(0.5)
        for i in range(value):
            send_cmd(FIRE)
            time.sleep(SLEEP_DURATION)
    else:
        print "Error: Unknown command: '%s'" % command


def run_command_set(commands):
    for cmd, value in commands:
        run_command(cmd, value)

def jenkins_target_user(user):
    thread.start_new_thread(play_sound, ('combined.wav', 0))
    match = False
    # Not efficient but our user list is probably less than 1k.
    # Do a case insenstive search for convenience.
    for key in USERS_COMMANDS_SEQUENCES:
        if key.lower() == user.lower():
            # We have a command set that targets our user so got for it!
            run_command_set(USERS_COMMANDS_SEQUENCES[key])
            match = True
            break
    if not match:
        print "WARNING: No target command set defined for user %s" % user


def read_url(url):
    request = urllib2.Request(url)

    if HTTPAUTH_USER and HTTPAUTH_PASS:
        authstring = base64.encodestring('%s:%s' % (HTTPAUTH_USER, HTTPAUTH_PASS))
        authstring = authstring.replace('\n', '')
        request.add_header("Authorization", "Basic %s" % authstring)

    return urllib2.urlopen(request).read()


def get_last_failed_build_datetime(job_name):
    changes_url = JENKINS_SERVER + "/job/" + job_name + "/lastFailedBuild"
    changedata = read_url(changes_url)
    m = re.compile('([0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2})').search(changedata)
    if m:
        date = datetime.datetime.strptime(m.group(1), '%Y-%m-%d_%H-%M-%S') #  2015-04-18_02-46-36
    else:
        date = datetime.datetime.now()

    return date

def jenkins_get_responsible_user(job_name):
    # Call back to Jenkins and determin who broke the build. (Hacky)
    # We do this by crudly parsing the changes on the last failed build
    
    changes_url = JENKINS_SERVER + "/job/" + job_name + "/lastFailedBuild/changes"
    changedata = ''
    try:
        changedata = read_url(changes_url)
    except urllib2.HTTPError, err:  
        if err.code == 404:
            print '404 error for [' +  changes_url + ']'
        else:
            raise


    # Look for the /user/[name] link
    m = re.compile('/user/([^/"]+)').search(changedata)
    if m:
        return m.group(1)
    else:
        return None


def jenkins_wait_for_event():

    # Data in the format: 
    #   {"name":"Project", "url":"JobUrl", "build":{"number":1, "phase":"STARTED", "status":"FAILURE" }}

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('10.0.100.29', JENKINS_NOTIFICATION_UDP_PORT)
    sock.bind(server_address)

    while True:
        data, addr = sock.recvfrom(8 * 1024)
        try:
            notification_data = json.loads(data)
            status = notification_data["build"]["status"].upper()
            phase  = notification_data["build"]["phase"].upper()
            if phase == "COMPLETED" and status == "FAILURE":
                job_name = notification_data["name"]
                last_failure_build_date = get_last_failed_build_datetime(job_name)
                # because of jenkins bug notifying about old failed builds - make sure that this failure is relevant
                if last_failure_build_date <= (datetime.datetime.now() - datetime.timedelta(minutes=5)):
                    print "%s Got an old notification about failed build. Job name - [%s]!" %(str(datetime.datetime.now()), notification_data["name"])
                    continue
                print "%s Got new notification about completed build that failed. Job name - [%s]!" %(str(datetime.datetime.now()), notification_data["name"])
                target = jenkins_get_responsible_user(job_name)
                if target == None:
                    print "%s WARNING: Could not identify the user who broke the build. Data - [%s]!" %(str(datetime.datetime.now()), str(notification_data))
                    continue

                print "Build Failed! Targeting user: " + target
                jenkins_target_user(target)
        except Exception, e:
            print 'Exception caught while waiting for build failure event. Exception - [%s]' %(str(e))
            pass
                

def main(args):

    if len(args) < 2:
        usage()
        sys.exit(1)

    # initialize Thunder USB device handle
    #setup_usb()

    if args[1] == "stalk":
        output_msg = "Listening and waiting for Jenkins build failure events of you and your loosy friends"
        if len(args) > 2 and args[2] == "tease":
            # the user has requested to activate random-shooting-mode as well s
            output_msg += " (but always expect suprises ;) )..."
            print output_msg
            shoot_once_a_while()
        else:
            print output_msg        
        
        jenkins_wait_for_event()
        # Will never return
        return

    # Process any passed commands or USERS_COMMANDS_SEQUENCES
    command = args[1]
    value = 0
    if len(args) > 2:
        value = int(args[2])

    if command in USERS_COMMANDS_SEQUENCES:
        run_command_set(USERS_COMMANDS_SEQUENCES[command])
    else:
        run_command(command, value)


if __name__ == '__main__':
    main(sys.argv)
    