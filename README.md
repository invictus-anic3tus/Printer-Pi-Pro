# Printer-Pi-Pro
The all-in-one Raspberry Pi hat for controlling your 3D printer!

<img src="https://github.com/invictus-anic3tus/Printer-Pi-Pro/blob/main/images/Printer-Pi-Pro_IMG1.png" alt="Title Image" width="100%" heigh="100%"></img>


The Printer Pi Pro is a Raspberry Pi hat plus a relay module. The hat controls things like servos, an accelerometer, a fan for cooling the pi, and more. It also controls a relay that can turn your printer on or off!

## Contents!! Yay!!
- [Printer-Pi-Pro](#printer-pi-pro)
- [Features](#features)
- [Setup](#setup)
  - [Music](#music)
  - [Input Shaping](#input-shaping)
  - [Servos](#servos)
  - [Fan](#fan)
  - [Relay](#relay)
- [Ordering](#ordering)
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

## Music:

How to play music with the buzzer on the Pi with a script: [https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/9](https://projects.raspberrypi.org/en/projects/introduction-to-the-pico/9) However, 3D printer firmware doesn't natively support running Raspberry Pi scripts using Gcode. In Klipper firmware, you can do it with Gcode with the [Gcode Shell Commands extension](https://github.com/dw-0/kiauh/blob/master/docs/gcode_shell_command.md). In Octoprint + Marlin, use [this](https://plugins.octoprint.org/plugins/gcodesystemcommands/). The buzzer here is connected to GPIO 3.

## Input Shaping:

If you don't already know, input shaping is the method of using an accelerometer to measure vibrations when moving the 3D printer parts at high speeds. Normally, these vibrations can cause ringing issues in the print, but with input shaping, the printer is able to compensate and use the vibrations and minimize ringing substantially. The ADXL345 connector on the board uses the same pinout as both of the below links do.

Input shaping for Octoprint + Marlin: [https://community.octoprint.org/t/octoprint-pinput-shaping-a-plugin-to-test-input-shaping-with-marlin/63089](https://community.octoprint.org/t/octoprint-pinput-shaping-a-plugin-to-test-input-shaping-with-marlin/63089)

Input shaping for Klipper: [https://www.klipper3d.org/Resonance_Compensation.html](https://www.klipper3d.org/Resonance_Compensation.html)

## Servos:

Servos are quite easy to control! Here's a good instructables guide: [https://www.instructables.com/Controlling-Servo-Motor-Sg90-With-Raspberry-Pi-4/](https://www.instructables.com/Controlling-Servo-Motor-Sg90-With-Raspberry-Pi-4/) You can control your shell scripts the same way you do with the buzzer scripts. You can use the servos to extend a Klicky docking arm, move a webcam, or clear the build plate. Servo 1 is connected to GPIO 13, and Servo 2 is connected to GPIO 19, which are both PWM pins.

## Fan:

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

## Relay
The relay port simply outputs 5V from the main power source, meaning it can draw up to 800mA through the 2N2222A transistor. You could actually use it for any low-power 5V device you wish, but I think most people will use it for a relay. You can use it to switch 24V from the PSU using a DC-DC relay, or, like I am, you can use it to switch an AC relay. Simply connect 5V to the input voltage on your relay, and GPIO2 to the ground. Note that this does _not_ go straight to GPIO2. I labelled it that simply as a reference as to which GPIO you should set in your script. In reality, it goes through a transistor circuit just like the fan's.

This port, however, does not have a PWM output like the fan does. You could attach a fan to it, but it could only run at 0% or 100%. So the on script (we'll call it relay-on.py) could look something like:

```
import RPi.GPIO as GPIO
import time

RELAY_PIN = 2 # we're using GPIO 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

GPIO.output(RELAY_PIN, GPIO.HIGH) # switch the relay on
```

You could put this simply in a folder like /home/pi/relay/ for easy access.

Pretty straightforward! However, where this feature can shine the most, is turning the printer on or off remotely. To do this, simply use this extension for Klipper: [Gcode Shell Commands extension](https://github.com/dw-0/kiauh/blob/master/docs/gcode_shell_command.md), or in Octoprint + Marlin, use [this one](https://plugins.octoprint.org/plugins/gcodesystemcommands/). You can use a script to turn the relay on (make sure not to call GPIO.cleanup()! It would turn the relay off at the end of the script) and one to turn it off, and add these as GCode commands in your printer's interface. But the issue here is, you can't run GCode while the printer is off! In this case, you'd have to SSH into the Pi and turn it on by manually running the script. Another thing you can do is make the on script start up when the Pi powers on, so that you only have to turn on the Pi and the printer turns on afterwards. First, open `/etc/systemd/system/` and create a new file such as `relay-on.service`. Paste the following:
```
[Unit]
Description=Turn GPIO2 Relay On
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=pi
ExecStart=/usr/bin/python3 /home/pi/relay/relay-on.py

[Install]
WantedBy=multi-user.target
```
Now you can enable it to startup every time the Pi boots! You can do this with `sudo systemctl enable relay-on.service`.

You can do the same thing for turning it off.

## Note:
if you do decide to use an AC relay with this, always be sure that shorts can never occur! AC voltage is really really powerful, and you could get badly injured if you don't wire it correctly. That's all!

# Ordering
The PCB Gerber files, BOM, and CPL (Pick-in-place) file are all in the PCB_Files folder. What I did was order just the PCB (not assembled) through JLCPCB, then combine it with an LCSC order as described [here](https://lcsc.com/faqs/notice?id=D2E15B9830B18723CDFFC807606915A6). Alternatively, you could order an assembled PCB, or a non-assembled PCB with the parts from a PCB place that lets you do that. JLC only gives you the parts if you buy the PCB assembled. All the parts can be ordered from LCSC. You can download the LCSC cart from the PCB_Files folder as well.

# Contributing
This is a pretty simple project, but if you have any ideas on things to add, anything in here that could be updated, etc, feel free to make an issue on this repo or email me! (email is in [my profile](https://github.com/invictus-anic3tus))

<img src="https://github.com/invictus-anic3tus/Printer-Pi-Pro/blob/main/images/Printer-Pi-Pro_IMG2.png" alt="Ending Image" width="100%" heigh="100%"></img>
