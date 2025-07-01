
# <img src="https://github.com/invictus-anic3tus/Printer-Pi-Pro/blob/main/images/Printer-Pi-Pro_TitleIMG.png" alt="Title Image" width="100%" heigh="100%"></img>

<h3 align="center">The all-in-one Raspberry Pi hat for controlling your 3D printer!</h3>

<p align="center">
  <img alt="Zero Vibe Coding" src="https://img.shields.io/badge/Zero-Vibe_Coding-blue?style=for-the-badge"></img>
  <img alt="Funded by Hack Club" src="https://img.shields.io/badge/Hack_Club-Funded-ec3750?style=for-the-badge&logo=hackclub&logoColor=ec3750"></img>
</p>





The Printer Pi Pro is a Raspberry Pi hat plus a relay module. The hat controls things like servos, an accelerometer, a fan for cooling the pi, and more. It also controls a relay that can turn your printer on or off!


## Contents!! Yay!!
- [Features](#features)
- [Setup](#setup)
  - [Buzzer](#music-with-the-buzzer)
  - [Fan](#controlling-the-fan)
  - [Servos](#controlling-servos)
  - [Input Shaping](#input-shaping-with-the-adxl345)
  - [Relay](#controlling-the-relay)
- [Ordering](#ordering)
  - [BOM](#bom) 
- [Contributing](#contributing)

## What you need:
1. A raspberry pi (duh) with Klipper or Octoprint installed (all features are compatible with both!)
2. The Printer Pi Pro PCB

If you aren't controlling anything with the PCB, that's all you need! However, you likely won't just make the PCB solely to put it on the Pi and not plug anything into it. So here's what you can do with it:

# Features:
1. Onboard passive buzzer: can create little tunes and jingles when your print starts, finishes, cancels, or anything else you want!
2. 5V Fan port: for active cooling your Raspberry Pi. You can code this to turn on when the Pi starts getting hot.
3. Two servo ports: perfect for pitch and yaw of a webcam! or anything else really
4. ADXL345 port: for an accelerometer and input shaping!
5. Relay port: to control an AC or DC relay. This can be for lights, or to turn on/off the printer. More on this later.

# Setup

![Wiring](https://github.com/invictus-anic3tus/Printer-Pi-Pro/blob/main/images/Printer-Pi-Pro_Wiring.jpg)

|Part   |Pins           |
|-------|---------------|
|Buzzer |PWM GPIO3      |
|Fan    |PWM GPIO18     |
|Servo 1|PWM GPIO13     |
|Servo 2|PWM GPIO19     |
|ADXL   |SPI Interface  |
|Relay  |GPIO2 (Not PWM)|

## Music with the buzzer

How to play music with the passive buzzer on the Pi with a script: [https://www.circuitbasics.com/how-to-use-buzzers-with-raspberry-pi/](https://www.circuitbasics.com/how-to-use-buzzers-with-raspberry-pi/) However, 3D printer firmware doesn't natively support running Raspberry Pi scripts using Gcode. In Klipper firmware, you can do it with Gcode with the [Gcode Shell Commands extension](https://github.com/dw-0/kiauh/blob/master/docs/gcode_shell_command.md). In Octoprint + Marlin, use [this](https://plugins.octoprint.org/plugins/gcodesystemcommands/). The buzzer here is connected to GPIO 3.

## Controlling the fan

The fan port is connected to a transistor circuit which turns the two-pin 5V fan on or off using GPIO 18. Additionally, using GPIO 18's PWM signal, you can put the fan at a percentage of speed, for example 25% speed when the Pi is at 40°C, 50% at 45°C, and so on. To change the PWM frequency via a Raspberry Pi script, simply use something like:

```
import RPi.GPIO as GPIO
import time

FAN_PIN = 18 # we're using GPIO 18
FREQ = 25000  # 25khz PWM frequency makes the fan smooth

GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT)

pwm = GPIO.PWM(FAN_PIN, FREQ)
pwm.start(0)  # Start with fan off

pwm.ChangeDutyCycle(25) # 25% speed
time.sleep(3)
pwm.ChangeDutyCycle(50) # 50% speed
time.sleep(3)
pwm.ChangeDutyCycle(75) # 75% speed
time.sleep(3)
pwm.ChangeDutyCycle(100) # 100% speed

pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()
```

There are more example scripts in the example_scripts folder!

## Controlling servos

Servos are quite easy to control! Here's a good instructables guide: [https://www.instructables.com/Controlling-Servo-Motor-Sg90-With-Raspberry-Pi-4/](https://www.instructables.com/Controlling-Servo-Motor-Sg90-With-Raspberry-Pi-4/) You can control your shell scripts the same way you do with the buzzer scripts. You can use the servos to extend a Klicky docking arm, move a webcam, or clear the build plate. Servo 1 is connected to GPIO 13, and Servo 2 is connected to GPIO 19, which are both PWM pins.

## Input shaping with the ADXL345

If you don't already know, input shaping is the method of using an accelerometer to measure vibrations when moving the 3D printer parts at high speeds. Normally, these vibrations can cause ringing issues in the print, but with input shaping, the printer is able to compensate and use the vibrations and minimize ringing substantially. The ADXL345 connector on the board uses the same pinout as both of the below links do.

Input shaping for Octoprint + Marlin: [https://community.octoprint.org/t/octoprint-pinput-shaping-a-plugin-to-test-input-shaping-with-marlin/63089](https://community.octoprint.org/t/octoprint-pinput-shaping-a-plugin-to-test-input-shaping-with-marlin/63089)

Input shaping for Klipper: [https://www.klipper3d.org/Resonance_Compensation.html](https://www.klipper3d.org/Resonance_Compensation.html)

## Controlling the relay

The relay port simply outputs 5V from the main power source, meaning it can draw up to 800mA through the 2N2222A transistor. You could actually use it for any low-power 5V device you wish, but I think most people will use it for a relay. You can use it to switch 24V from the PSU using a DC-DC relay, or, like I am, you can use it to switch an AC relay. Simply connect 5V to the input voltage on your relay, and GPIO2 to the ground. Note that this does _not_ go straight to GPIO2. I labelled it that simply as a reference as to which GPIO you should set in your script. In reality, it goes through a transistor circuit just like the fan's.

This port, however, does not have a PWM output like the fan does. You could attach a fan to it, but it could only run at 0% or 100%. So the on/handle-interupts script (we'll call it relay-service.py) could look something like:

```
import RPi.GPIO as GPIO
import time
import signal
import sys

RELAY_PIN = 2 # we're using GPIO 2

def cleanup(sig, frame)
    GPIO.cleanup() # this sets everything low, turning off the relay
    sys.exit(0) # exits with success

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH) # switch the relay on

signal.signal(signal.SIGINT, cleanup) # this handles Ctrl+C's and other interruptions
signal.signal(signal.SIGTERM, cleanup) # this handles systemd's termination signals

while True: # this doesn't let the script turn off until it's interrupted or ended
    time.sleep(1) # wait for one second between loops, so as not to overload the system lol
```

You could put this simply in a folder like /home/pi/relay/ for easy access.

Next, we have to make an off script, like the following:

```
import RPi.GPIO as GPIO

RELAY_PIN = 2 # we're using gpio 2
GPIO.setmode(GPIO.BCM) # use gpio numbers instead of pin numbers
GPIO.setup(RELAY_PIN, GPIO.OUT) # set it to be an output
GPIO.output(RELAY_PIN, GPIO.LOW) # turn it off
GPIO.cleanup() # clean up and exit gracefully
```

Now, make the systemd service. You can make the relay start up when the Pi powers on, so that you only have to turn on the Pi and the printer turns on afterwards. First, open `/etc/systemd/system/` and create a new file such as `relay-control.service`. Paste the following:

```
[Unit]
Description=GPIO2 Relay Controller
After=network.target

[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=/usr/bin/python3 /home/pi/relay/relay-service.py
ExecStop=/usr/bin/python3 /home/pi/relay/relay-off.py

[Install]
WantedBy=multi-user.target
```

What the above does is setup a service, just like Klipper is a service and Crowsnest is a service. It sets it to be simple, meaning it doesn't fork. It always restarts if it stops or crashes, and waits a second between attempts. It runs the script as the user pi (replace this with your admin user) and when starting, runs relay-service.py, and when it's stopped it runs relay-off.py. This means that when you first start the script, i.e., on boot, it runs relay-service.py, turning on the relay, and when you run the command to stop it, `sudo systemctl stop relay-control`, or if you power off the pi, it powers off the relay using relay-off.py or through relay-service.py's cleanup() function.

Now, if you want to, you can first reload systemd with `sudo systemctl daemon-reload`, and then enable the service to start up every time the Pi boots! You can do this with `sudo systemctl enable relay-control`. This won't start it immediately after running; to do that you can run `sudo systemctl start relay-control`.

Pretty straightforward! However, where this feature can shine the most, is turning the printer on or off remotely. To do this, simply use this extension for Klipper: [Gcode Shell Commands extension](https://github.com/dw-0/kiauh/blob/master/docs/gcode_shell_command.md), or in Octoprint + Marlin, use [this one](https://plugins.octoprint.org/plugins/gcodesystemcommands/). You can add the commands `sudo systemctl start relay-control` to turn it on and `sudo systemctl stop relay-control` to turn it off as GCode commands in your printer's interface. But the issue here is, you can't run GCode while the printer is off! In this case, you'd have to SSH into the Pi and turn it on by manually running the script, or simply reboot the Pi if you've configured the service to start on boot.

## Note:
if you do decide to use an AC relay with this, always be sure that shorts can never occur! AC voltage is really really powerful, and you could get badly injured if you don't wire it correctly. That's all!

# Ordering
The PCB Gerber files, BOM, and CPL (Pick-in-place) file are all in the PCB_Files folder. What I did was order just the PCB (not assembled) through JLCPCB, then combine it with an LCSC order as described [here](https://lcsc.com/faqs/notice?id=D2E15B9830B18723CDFFC807606915A6). Alternatively, you could order an assembled PCB or buy a PCB with the parts not assembled. Unfortunately, JLC only gives you the parts if you buy the PCB assembled. All the parts can be ordered from LCSC; you can also download the cart from the PCB_Files folder.

You'll also need some JST-XH wire housings to fit into the ports on the PCB. If you're combining an LCSC order and a JLCPCB order as mentioned above, you can simply add these to the cart. For example, [this](https://lcsc.com/product-detail/Housings-Wire-To-Board-Wire-To-Wire_JST-XHP-6_C144405.html) is a 6-pin housing to fit into the ADXL345 port. If you're getting an assembled PCB from JLCPCB, you'll have to buy the housings separately, whether through JLCPCB's part cart or a seller such as AliExpress or Amazon.

Also, keep in mind that there's only one component on the bottom side of the PCB: the Raspberry Pi pinheader. This was another reason I bought from LCSC and combined the shipping with JLCPCB, because if I had gotten an assembled PCB from JLC, I would've had to either get a double-sided PCB or put the header on the front, desolder it, and re-solder it onto the back. The PCB also has 4 SMD components. They aren't anything super hard to solder, just two 0805 size resistors and two SOD123F size diodes.

## BOM
|Part               |Link                                                                                              |Per Part|Quantity      |Total                  |
|-------------------|--------------------------------------------------------------------------------------------------|--------|--------------|-----------------------|
|PCB (No parts)     |https://jlcpcb.com                                                                                |$2.10   |1             |$2.10                  |
|1N4148W Diode      |https://lcsc.com/product-detail/image/1N4148W_C81598.html                                         |$0.01   |50            |$0.54                  |
|6P JST-XH Port     |https://lcsc.com/product-detail/Wire-To-Board-Connector_JST-B6B-XH-A-GU_C265366.html              |$0.42   |5             |$2.11                  |
|2P JST-XH Port     |https://lcsc.com/product-detail/image/B2B-XH-A-LF-SN_C158012.html                                 |$0.03   |20            |$0.69                  |
|0805 Resistor      |https://lcsc.com/product-detail/Chip-Resistor-Surface-Mount_Viking-Tech-ARG05FTC5000_C2828857.html|$0.01   |50            |$0.45                  |
|2N2222A Transistor |https://lcsc.com/product-detail/image/2N2222A_C5330385.html                                       |$0.02   |50            |$0.87                  |
|Passive Buzzer     |https://lcsc.com/product-detail/image/YS-MBZ12085C05R42_C409842.html                              |$0.14   |5             |$0.68                  |
|3P Pinheader       |https://lcsc.com/product-detail/image/PZ254V-11-03P_C2937625.html                                 |$0.02   |50            |$0.75                  |
|2x20P Socket header|https://lcsc.com/product-detail/image/2-54-2-20_C2977589.html                                     |$0.19   |5             |$0.97                  |
|6P JST-XH Housing  |https://lcsc.com/product-detail/image/XHP-6_C144405.html                                          |$0.03   |20            |$0.52                  |
|AC Relay           |https://www.amazon.com/gp/product/B08GPB7N2T/                                                     |$11.79  |1             |$11.79                 |
|5V DC Fan          |https://lcsc.com/product-detail/image/MF40100V2-1000C-A99_C456919.html                            |$2.59   |1             |$2.59                  |
|-------------------|                                                                                                  |--------|              |-----------------------|
|                   |                                                                                                  |        |Total         |$24.05                 |
|                   |                                                                                                  |        |Shipping + Tax|~$20 (merging JLC+LCSC)|


# Contributing
This is a pretty simple project, but if you have any ideas on things to add, anything in here that could be updated, etc, feel free to make an issue on this repo or email me! (email is in [my profile](https://github.com/invictus-anic3tus))

<img src="https://github.com/invictus-anic3tus/Printer-Pi-Pro/blob/main/images/Printer-Pi-Pro_IMG2.png" alt="Ending Image" width="100%" heigh="100%"></img>
