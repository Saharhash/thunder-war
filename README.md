# thunder-war
Dream Cheeky Thunder cool shooter wrapper

# Main Features
Except for shooting at bad build breakers, it also shoots a given user, or shoots once a random time.

# Usage Scenarios
## Jenkins stalk
<b> Why? </b> 
* Your co-developers should know better when they git-push
* You want to get promotion and that people will ask about that "amazing guy that since he made this missle-luancher thing - the build never fails again!!"
<br>

<b> How? </b> <br>
thunder.py stalk


## Jenkins stalk & tease
<b> Why? </b> 
* Shoots once a random time, between working hours (9:30am - 6:30pm), at a random innocent friend
* Your team DOES NOT fail builds
* You still want some action in your office
* It`s funny when someone get shot for no reason (with FOAM darts ah??)
<br>

<b> How? </b> 
thunder.py stalk tease

## Single colleague shot
<b> Why? </b> 
* Your colleague annoyed you
* Your colleague broke the build and wasn`t present at the moment of shooting
* Your colleague just shot you with a Nerf gun
<br>

<b> How? </b> 
thunder.py [USERNAME]

## Other commands
You can always use one of the following commands
  * <b>fire</b> - fires a dart. <b>Optional</b> - number of darts<br>
  <b>e.g</b> - thunder.py fire 2
  
  * reset / zero</b> - move canon to zero position (bottom-left)<br>
  <b>e.g</b> - thunder.py zero
  
  * <b>right</b> - move canon right <value> milliseconds<br>
  <b>e.g</b> - thunder.py right 500 
  
  * <b>left</b> - move canon left <value> milliseconds<br>
  <b>e.g</b> - thunder.py left 300

  * <b>up</b> - move canon up <value> milliseconds<br>
  <b>e.g</b> - thunder.py up 250

  * <b>down</b> - move canon down <value> milliseconds<br>
  <b>e.g</b> - thunder.py down 200

  * <b>led</b> - turns the led on/off<br>
  <b>e.g</b> - thunder.py led 1
  
# Installation & Environment
## Client (Computer connected to thunder cheecky)
Generally if you want to use ThunderCheecky API
###Requirements: 
1. Dream Cheeky Thunder USB Missile Launcher
2. Python 2.6+
3. Python PyUSB Support and its dependencies 
http://sourceforge.net/projects/pyusb/
4. (Assuming you have Windows 64bit platform)
  1. Download libusb 
  http://sourceforge.net/projects/libusb-win32/<br>
  2. Download and extract the bin zip file (should go by the name of libusb-win32-bin)<br>
  3. Copy the dll from .\bin\x86\libusb0_x86.dll to C:\Windows\System32 and rename it libusb0.dll<br>
  4. Run .\bin\inf-wizard.exe and put 0x2123 as ProductId and 0x1010 as VendorId, which are the ThunderCheecky identifiers
  5. Press next, and then next again, and then Install Now
  6.Now we need to update our ThunderCheecky device so it will work with our driver
    1. Open Device Manager (winkey + PAUSE)
    2. Search for our USB device under Humen Interfaces. How to find it? You need to find ThunderCheecky details when you right click on marked interface -> details -> Choose Harderware Ids on the list. 
 Then search for the ids we`ve entered in step 4
    3. Once you`ve found our beloved thunder cheecky usb interface, go back to device manager, right click it, and then "Update driver"
    4. Choose the driver we`ve created on step 4
5. Let the games begin :)

#### Some other guides made by cool people
* http://community.spiceworks.com/how_to/1484-finding-drivers-by-vendor-and-device-id-s-through-devie-manager
* http://coffeefueledcreations.com/blog/?p=131
    
### Script adjustments
* Users & their locations - in order to add more users and change their locations, modify USERS_COMMANDS_SEQUENCES dictionary inside the python script. Just use the directions commands. <b> a WARM suggestion </b> - do the location adjustments after work hours so when you will finish, people will be amazed. Also, I love to use the "pause" command inside a sequence, right before the shooting. It makes your target do weird faces and stand in defensive position
* Change your Jenkins settings
  ** JENKINS_NOTIFICATION_UDP_PORT - the port you will set in your Jenkins job. This port will be opened on your machine and will receive notifications from Jenkins
  ** JENKINS_SERVER - Jenkins server`s IP

## Jenkins
1. Choose your desired project and press `Configure`
2. Under `Job Notifications`, press `Add Endpoint`
3. Fill the following details
  * Format - Json
  * Protocol - UDP
  * Event - Job Completed
  * URL - {YOUR_THUNDER_CHEECKY_MACHINE_SCRIPT_IP}:{YOUR_THUNDER_CHEECKY_MACHINE_SCRIPT_PORT}
  * TIMEOUT - 30000
  * LOG - 1 (I know that you don\`t want any log lines, but apprently Jenkins Notifications Plugin has a bug that when there is not log lines to send, it doesn\`t send any notification)
4. `Save` (Configuration)

# Credits
My project is based on Chris Dance retailiation script. Chris --> You`re awesome!
  
