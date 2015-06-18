# thunder-war
Dream Cheeky Thunder cool shooter wrapper

# Main Features
Except for shooting at bad build breakers, it also shoots a given user (given as a parameter), or shoots once a random time.

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

# Installation & Environment
Generally if you want to use ThunderCheecky API
## Requirements: 
  1. A Dream Cheeky Thunder USB Missile Launcher
  2. Python 2.6+
  3. Python PyUSB Support and its dependencies 
      http://sourceforge.net/projects/pyusb/
  4. (Assuming you have Windows 64bit platform)
  4.1. Download libusb 
      http://sourceforge.net/projects/libusb-win32/
  4.2. Download and extract the bin zip file (should go by the name of libusb-win32-bin)
  4.3. Copy the dll from .\bin\x86\libusb0_x86.dll to C:\Windows\System32 and rename it libusb0.dll
  4.4. Run .\bin\inf-wizard.exe and put 0x2123 as ProductId and 0x1010 as VendorId, which are the ThunderCheecky identifiers
  4.5. Press next, and then next again, and then Install Now
  4.6. Now we need to update our ThunderCheecky device so it will work with our driver
  4.6.1. Open Device Manager (winkey + PAUSE)
  4.6.2. Search for our USB device under Humen Interfaces. How to find it? You need to find ThunderCheecky details when you right click on marked 
  

# Adjustment


